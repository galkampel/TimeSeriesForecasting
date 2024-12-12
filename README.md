# Time Series Analysis
* In this repository, I investigate point and probabilistic forecasting models using Darts and GluonTS, using static and dynamic features, backtesting and present a technique for dealing with missing/extreme values

## Point Forecasts
* Forecast a single point
* Models- ARIMA, Linear Regression

## Probabilistic Forecasts
* Each forecast point comes from some underlying distribution
* We can represent confidence interval to quantify the uncertainty
* Models- NPTS, DeepAR

## Missing Values Imputations and Dealing with Extreme Values
* Use backtesting and a probabilistic models to impute missing values (and cap missing values)

## Darts installation notes
conda install:
* Install darts with all available models (recommended): conda install -c conda-forge -c pytorch u8darts-all.
* Install core + neural networks (PyTorch): conda install -c conda-forge -c pytorch u8darts-torch
* Install core only (without neural networks or AutoARIMA): conda install -c conda-forge u8darts

pip install:
* Install darts with all available models: pip install darts
* Install core only (without neural networks, Prophet or AutoARIMA): pip install u8darts
* Install core + neural networks (PyTorch): pip install "u8darts[torch]"
* Install core + AutoARIMA: pip install "u8darts[pmdarima]"
