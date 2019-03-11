Pangeo's BinderHub
==================

Deployment and configuration documentation files for the public binder.pangeo.io service.


# Deployment Status

Branch | Build | Docs
-- |-- | --
staging | [![CircleCI](https://circleci.com/gh/pangeo-data/pangeo-binder/tree/staging.svg?style=svg)](https://circleci.com/gh/pangeo-data/pangeo-binder/tree/staging) | [![Documentation Status](https://readthedocs.org/projects/pangeo-binder/badge/?version=staging)](https://pangeo-binder.readthedocs.io/en/staging/?badge=staging)
prod | [![CircleCI](https://circleci.com/gh/pangeo-data/pangeo-binder/tree/prod.svg?style=svg)](https://circleci.com/gh/pangeo-data/pangeo-binder/tree/prod) | [![Documentation Status](https://readthedocs.org/projects/pangeo-binder/badge/?version=prod)](https://pangeo-binder.readthedocs.io/en/prod/?badge=prod)


# About Pangeo's Binder

Much like [mybinder.org](https://mybinder.org), the [Pangeo's](https://pangeo.io/) BinderHub deployment ([binder.pangeo.io](https://binder.pangeo.io/)) allows users to create and share custom computing environments. The main distinction between the two BinderHubs is that Pangeo's BinderHub allows users to perform scalable computations using the dask-kubernetes package.

For more information on the Pangeo project, check out the [online documentation](http://pangeo-binder.readthedocs.io/).

## How to deploy:
This repo is continuously deployed using [CircleCI](https://circleci.com/gh/pangeo-data/pangeo-binder). It can also be deployed from a local computer using the following command:
```
cd helm-chart
deployment={staging,prod}  # choose one
helm upgrade --wait --install --namespace=${deployment} ${deployment} \
    pangeo-binder --version=v0.2.0 \
    -f ../deploy/${deployment}.yaml \
    -f ../secrets/${deployment}.yaml
```