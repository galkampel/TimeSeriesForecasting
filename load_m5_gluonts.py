# Works on gluonts dev branch as of May 30th, 2023
# Assumes "m5-forecasting-accuracy" folder with data next to the script
# Data is obtained from https://www.kaggle.com/c/m5-forecasting-accuracy

import pandas as pd
from pathlib import Path
from gluonts.dataset.pandas import PandasDataset

# Load data from csv files

cal = pd.read_csv(
    Path(__file__).parent / "m5-forecasting-accuracy" / "calendar.csv",
)
weekly_prices = pd.read_csv(
    Path(__file__).parent / "m5-forecasting-accuracy" / "sell_prices.csv",
)
sales_and_features = pd.read_csv(
    Path(__file__).parent
    / "m5-forecasting-accuracy"
    / "sales_train_validation.csv",
)

# Check data

assert len(sales_and_features["item_id"].unique()) == 3049
assert len(sales_and_features["store_id"].unique()) == 10
assert len(sales_and_features) == 30490

# We want to split the data into static (categorical features) vs dynamic (sales data).
# We keep the 'id' column in both, to be able to join the two.
# We also keep 'item_id' and 'store_id' in the sales data, to be able to join with prices later.

features_columns = ["id", "dept_id", "cat_id", "store_id", "state_id"]
sales_columns = ["id", "item_id", "store_id"] + [
    f"d_{k}" for k in range(1, 1914)
]

features = (
    sales_and_features[features_columns].set_index("id").astype("category")
)
sales = sales_and_features[sales_columns]

assert len(features) == 30490
assert len(features.columns) == 4
assert len(sales) == 30490
assert len(sales.columns) == 1916

# Turn sales data into long format, to join with prices more easily.

sales_long = sales.melt(
    id_vars=["id", "item_id", "store_id"], var_name="d", value_name="sales"
)

# To join sales data with prices, first we add the `"wm_yr_wk"` column from `cal`.
# We also add the `"date"` column to build the time index.
# Then we join with `weekly_prices` on `"store_id"`, `"item_id"`, `"wm_yr_wk"`,
# to get the `"sell_price"` column in.

temp = sales_long.merge(
    cal[["d", "wm_yr_wk", "date"]],
    on="d",
    how="left",
    suffixes=(None, "_right"),
)

sales_with_prices = temp.merge(
    weekly_prices,
    on=["store_id", "item_id", "wm_yr_wk"],
    how="left",
    suffixes=(None, "_right"),
)

sales_with_prices.index = pd.to_datetime(sales_with_prices["date"])

# Some rows have missing price, which means the item was not for sale.
# Let's replace price there with some constant, and add a column indicating
# whether the product was for sale on that date.

sales_with_prices["for_sale"] = 1.0 * sales_with_prices["sell_price"].notna()
sales_with_prices["sell_price"].fillna(0.0, inplace=True)

# We're ready to construct our dataset object.

dataset = PandasDataset.from_long_dataframe(
    sales_with_prices,
    item_id="id",
    target="sales",
    feat_dynamic_real=["sell_price", "for_sale"],
    static_features=features,
)

assert len(dataset) == 30490

print(dataset)

print(next(iter(dataset)))