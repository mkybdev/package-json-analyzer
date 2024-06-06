import pandas as pd
from tqdm import tqdm  # type: ignore

from package_json_analyzer.cooccurrence.make_heatmap import make_heatmap  # type: ignore
from package_json_analyzer.cooccurrence.make_network import make_network  # type: ignore

from .get_probability import get_probability
from .get_conditional_probability import get_conditional_probability
from ..common.format_df import format_df
from ..common.logger import *
from ..common.export_df import export_df


class Cooccurrence:
    def __init__(self, df: pd.DataFrame, cols: list[str]):
        if not set(cols).issubset(df.columns):
            error(f"All columns: {cols} must be in the input data.")
        self.df = df
        self.cols = cols
        self.formatted_df = format_df(df, cols)

    def conditional_probability(self) -> dict[str, pd.DataFrame]:
        return get_conditional_probability(
            self.formatted_df,
            {
                str(name): get_probability(series)
                for name, series in self.formatted_df.items()
            },
            self.cols,
        )

    def run(self):
        print()
        conditional_probabilities = self.conditional_probability()
        for key, value in tqdm(
            conditional_probabilities.items(), desc="RUNNING COOCCURRENCE ANALYSIS"
        ):
            export_df(
                value, "cooccurrence/conditional_probability", f"{key}", quiet=True
            )
        print()
        make_heatmap(conditional_probabilities)
        print()
        make_network(conditional_probabilities)
