"""
A viewer for Stats objects.
"""
import os
from itertools import chain

from IPython.display import display_html, display
from IPython.html.widgets import interactive, IntSliderWidget
import matplotlib.pyplot as plt
import pandas as pd
from pstats import Stats
from six import iteritems
import seaborn as sns
sns.set_palette("deep", desat=.6)

timing_colnames = [
    "filename",
    "lineno",
    "funcname",
    "ccalls",
    "ncalls",
    "tottime",
    "cumtime",
]

caller_columns = [
    "filename",
    "lineno",
    "funcname",
    "caller_filename",
    "caller_lineno",
    "caller_funcname",
    "ccalls",
    "ncalls",
    "tottime",
    "cumtime",
]


def _calc_frames(stats):
    """
    Compute a DataFrame summary of a Stats object.
    """
    timings = []
    callers = []
    for key, values in iteritems(stats.stats):
        timings.append(
            pd.Series(
                key + values[:-1],
                index=timing_colnames,
            )
        )
        for caller_key, caller_values in iteritems(values[-1]):
            callers.append(
                pd.Series(
                    key + caller_key + caller_values,
                    index=caller_columns,
                )
            )

    timings_df = pd.DataFrame(timings)
    callers_df = pd.DataFrame(callers)
    timings_df['filename:funcname'] = \
        timings_df['filename'] + ':' + timings_df['funcname']
    timings_df = timings_df.groupby('filename:funcname').sum()
    return timings_df, callers_df


class StatsViewer(object):

    default_view_fields = [
        "ncalls",
        "tottime",
        "cumtime",
    ]

    def __init__(self, filename, strip_dirs=True):
        self.name = os.path.basename(filename)
        stats = Stats(filename)
        self.stats = stats.strip_dirs() if strip_dirs else stats
        self.timings, self.callers = _calc_frames(stats)

    def summary(self, count):
        fig = plt.figure()
        fields = ['tottime', 'cumtime', 'ncalls']
        plot_locs = [311, 312, 313]
        for field, loc in zip(fields, plot_locs):
            data = self._get_timing_data(count, field, field)
            self._show_timing_data(data, field, ax=fig.add_subplo(loc))

    def _get_timing_data(self, count, sort, fields):
        data = self.timings.sort(
            sort,
            ascending=False
        )[fields].head(count)
        return data

    def _make_title(self, nrows, sort):
        names_by_sort = {
            "tottime": "Total Time",
            "cumtime": "Cumulative Time",
            "ncalls": "Call Count",
        }

        return "Top {}: {}".format(nrows, names_by_sort[sort])

    def _show_timing_data(self, data, sort, **mpl_kwargs):
        default_mpl_kwargs = {
            'figsize': (14, 10),
            'kind': 'barh',
            'title': self._make_title(len(data), sort),
        }
        default_mpl_kwargs.update(mpl_kwargs)
        data.plot(
            **default_mpl_kwargs
        )
        if sort in ('tottime', 'cumtime'):
            plt.xlabel('Seconds')
        elif sort == 'ncalls':
            plt.xlabel('Call Count')
        plt.ylabel('Filename:Function Name')

    def view(self,
             count,
             sort,
             fields=None,
             show_table=True,
             show_graph=True,
             return_data=False,
             **mpl_kwargs):

        if fields is None:
            fields = self.default_view_fields
        data = self._get_timing_data(count, sort, fields)

        if show_table:
            # HACK: Make pandas always show an HTML Table repr for this frame.
            data._repr_fits_horizontal_ = lambda *args, **kwargs: True
            display_html(data._repr_html_(), raw=True)

        if show_graph:
            self._show_timing_data(
                data.ix[::-1, sort],
                sort,
                **mpl_kwargs
            )

        if return_data:
            return data

    def compare(self, other, field='cumtime', count=35):
        left = self._get_timing_data(count, field, field)
        left.name = "left"
        right = other._get_timing_data(count, field, field)
        right.name = "right"

        fig = plt.figure()
        self._show_timing_data(
            left[::-1],
            field,
            ax=fig.add_subplot('131')
        )
        self._show_timing_data(
            right[::-1],
            field,
            ax=fig.add_subplot('133')
        )

        data = pd.concat([left, right], axis=1).fillna(0)
        data['diff'] = data['left'] - data['right']
        data = data.sort('diff', ascending=False)

        # HACK: Make pandas always show an HTML Table repr for this frame.
        data._repr_fits_horizontal_ = lambda *args, **kwargs: True
        display_html(data._repr_html_(), raw=True)

    def interact(self):
        def _interact(count, field):
            self.view(count, field)

        display(
            interactive(
                _interact,
                count=IntSliderWidget(min=5,max=100,step=5,value=35),
                field=('cumtime', 'tottime', 'ncalls'),
            )
        )
