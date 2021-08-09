""" sth """
##
import os
import shutil
import pandas as pd


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def make_balanced_subsample(df: pd.DataFrame,
                            col2balance_across: str,
                            target_column: str):
    """ Makes the balanced subsample of df across col2balance, it finds all target values that have at least one observation for each value of col2balance
        Returns the common target values
        """

    x = col2balance_across
    y = target_column

    common_y = set(df[y].unique())

    for _, gp in df.groupby([x]).__iter__():
        common_y &= set(gp[y].unique())

    bs = df[df[y].isin(common_y)]
    return bs
