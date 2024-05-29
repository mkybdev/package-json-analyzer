import pandas as pd

from .get_probability import get_probability
from .get_conditional_probability import get_conditional_probability
from .format_df import format_df


class Cooccurrence:
    def __init__(self, df: pd.DataFrame, cols: list[str]):
        self.df = df
        self.cols = cols
        self.formatted_df = format_df(df, cols)

    def conditional_probability(self) -> pd.DataFrame:
        return get_conditional_probability(
            self.df, self.formatted_df.apply(get_probability).tolist(), self.cols
        )
