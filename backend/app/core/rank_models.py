import pandas as pd
from sklearn.isotonic import IsotonicRegression


class IsotonicRankRegressor:
    """Monotonic marks-to-rank curve for small rank datasets."""

    def __init__(self) -> None:
        self.model = IsotonicRegression(increasing=False, out_of_bounds="clip")

    def fit(self, x: pd.DataFrame, y: pd.Series) -> "IsotonicRankRegressor":
        self.model.fit(x["normalized_marks"], y)
        return self

    def predict(self, x: pd.DataFrame) -> pd.Series:
        return self.model.predict(x["normalized_marks"])
