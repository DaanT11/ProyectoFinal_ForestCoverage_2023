# ProyectoFinal_ForestCoverage_2023

Based on the data recollected from the Theodore Roosevelt National Park, we present the code and artifacts used to get the final multiclass prediction per wilderness zone as well as the input to create the final dashboards.

Brief Summary
Repository to share the code based on ITAM MSc in Data Science final assignement from Large Scale Methods course.

Requirements
All scrpts are based on python langaguage greater than 3.1 version, the only strict requirement is to have at least 1.2.0 scklearn version, an account on AWS with free Tier and access to the QuickSight tool to use final prediction table as the input.

Review the environments.yaml file to use with conda. Use the following command to re-create the current project conda environment: conda env create --file environments.yaml

Data
Data can be downloaded from Kaggle: [www.kaggle.com](https://www.kaggle.com/datasets/uciml/forest-cover-type-dataset)

Repo Structure
- data: files from train and test in csv format.
- plots: plots from eda
- msc: empty
- results: predictions in csv format
- src: Four .py scripts to explore, clean, process and predict.
- logs: has the log file to catch errors and info.

Usage
Main .py file will call the other modules and just be sure to have files in the same folder.
