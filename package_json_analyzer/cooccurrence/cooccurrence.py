import pandas as pd

from .get_probability import get_probability
from .get_conditional_probability import get_conditional_probability
from ..common.format_df import format_df
from ..common.logger import *


class Cooccurrence:
    def __init__(self, df: pd.DataFrame, cols: list[str]):
        if not set(cols).issubset(df.columns):
            error(f"All columns: {cols} must be in the input data.")
        self.df = df
        self.cols = cols
        self.formatted_df = format_df(df, cols)

    def conditional_probability(self) -> pd.DataFrame:
        return get_conditional_probability(
            self.formatted_df,
            {
                str(name): get_probability(series)
                for name, series in self.formatted_df.items()
            },
            self.cols,
        )
