import cProfile

import pandas as pd
import numpy as np

def naive_concat_dataframes():

    df1 = pd.DataFrame(
        np.random.randn(1000, 26),
        columns=[chr(ord('A') + i) for i in range(26)],
        index=range(1000),
    )

    df2 = pd.DataFrame(
        np.random.randn(1000, 26),
        columns=[chr(ord('A') + i) for i in range(26)],
        index=range(1000, 2000),
    )

    return pd.concat([df1, df2])

def fast_concat_dataframes():

    df1 = pd.DataFrame(
        np.random.randn(1000, 26),
        columns=[chr(ord('A') + i) for i in range(26)],
        index=np.arange(1000),
    )

    df2 = pd.DataFrame(
        np.random.randn(1000, 26),
        columns=[chr(ord('A') + i) for i in range(26)],
        index=np.arange(1000, 2000),
    )

    return pd.DataFrame(
        np.vstack([df1.values, df2.values]),
        columns=df1.columns,
        index=np.hstack(
            [
                df1.index.values,
                df2.index.values,
            ],
        ),
    )


if __name__ == '__main__':
    cProfile.runctx(
        'naive_concat_dataframes()',
        globals(),
        locals(),
        'naive.stats',
    )
    cProfile.runctx(
        'fast_concat_dataframes()',
        globals(),
        locals(),
        'fast.stats',
    )
