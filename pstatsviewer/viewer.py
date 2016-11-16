"""
A viewer for Stats objects.
"""
import os

from IPython.display import display
from ipywidgets import interactive, IntSlider
import matplotlib.pyplot as plt
import pandas as pd
from pstats import Stats
from qgrid.grid import show_grid
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
        (timings_df['filename'] + ':' + timings_df['funcname'])
    timings_df = timings_df.groupby('filename:funcname').sum()
    return timings_df, callers_df


class StatsViewer(object):

    default_view_fields = [
        "ncalls",
        "tottime",
        "cumtime",
    ]

    def __init__(self, filename, strip_dirs=True, remote_js=False):
        self.name = os.path.basename(filename)
        stats = Stats(filename)
        self.stats = stats.strip_dirs() if strip_dirs else stats
        self.timings, self.callers = _calc_frames(stats)
        self.remote_js = remote_js

    def summary(self, count):
        fig = plt.figure()
        fields = ['tottime', 'cumtime', 'ncalls']
        plot_locs = [311, 312, 313]
        for field, loc in zip(fields, plot_locs):
            data = self._get_timing_data(count, field, field)
            self._show_timing_data(data, field, ax=fig.add_subplo(loc))

    def _get_timing_data(self, count, sort, fields):
        data = self.timings.sort_values(
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
            'figsize': (12, 7),
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

    def _show_table(self, data):
        return show_grid(data, remote_js=self.remote_js)

    def table(self, fields=None):
        if fields is None:
            fields = self.default_view_fields

        data = self.timings[fields]
        return self._show_table(data)

    def chart(self, fields=None, **mpl_kwargs):

        if fields is None:
            fields = self.default_view_fields

        def _interact(count, sort_by):
            data = self._get_timing_data(count, sort_by, fields)
            self._show_timing_data(
                data.ix[::-1, sort_by],
                sort_by,
                **mpl_kwargs
            )

        return interactive(
            _interact,
            count=IntSlider(min=5, max=100, step=5, value=20),
            sort_by=('cumtime', 'tottime', 'ncalls'),
        )

    def compare_chart(self, other, field='cumtime', count=35):
        left = self._get_timing_data(count, field, field)
        right = other._get_timing_data(count, field, field)

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

    def compare_table(self, other, lsuffix='_l', rsuffix='_r'):

        left = self.timings[self.default_view_fields]
        right = other.timings[self.default_view_fields]

        return self._show_table(
            left.join(
                right,
                lsuffix=lsuffix,
                rsuffix=rsuffix,
            ).sort_index(axis=1)
        )

    def interact(self):
        def _interact(count, field):
            self.view(count, field, show_table=False)

        return display(
            show_grid(self.timings, self.remote_js),
            interactive(
                _interact,
                count=IntSlider(min=5, max=100, step=5, value=35),
                field=('cumtime', 'tottime', 'ncalls'),
            ),
        )
