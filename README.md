#GenomicsFeatures
###Analysis of Genomics Feature Matrices

This project contains a Google App Engine application written in Python that performs the following tasks:
  - Converts an *n* x *m* feature matrix in tsv format into a file in csv format with *n* x *m* rows of tuples (feature, sample, value) - `run_fmx_convert.py`
  - Builds a model for this data in Datastore - `model.py`
  - Runs a map-only MapReduce job to import the csv file you converted from GCS and into the model - `pipeline.py`
    - Data can also be imported via the bulkload mechanism but this is very slow. - `run_upload_data.sh` 
  - Defines and builds full text search index over the feature names. - `search.py`
  - Provides a User Interface that allows you to do the following: - `main.py`
    - Perform most of the admin tasks listed above.
    - Find features by using the full text search.
    - Pull up samples and their values for a given feature, including a chart that graphs the distribution of the values.
    - Fetch the value for a given sample and feature.
  - Provides a simple REST API that lets you select features and samples and will return their values. `main.py`
  - An example R script that can be used to call the API to fetch feature matrix data and perform analysis on this in R. - `Analysis.R`

This application can be run in both Google App Engine (Classic) or in a Google Managed VM via Docker.
