# Time Series Analysis
* Darts
* GluonTS


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