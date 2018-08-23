FROM jupyter/scipy-notebook

LABEL maintainer="wednesday.developer@gmail.com"

RUN conda install --quiet --yes -c conda-forge pystan fbprophet tqdm plotnine
