Pangeo's BinderHub
==================

Deployment and configuration documentation files for the public binder.pangeo.io service.


# Deployment Status

Branch | Build | Docs | Deployment
-- |-- | -- | --
staging | [![CircleCI](https://circleci.com/gh/pangeo-data/pangeo-binder/tree/staging.svg?style=svg)](https://circleci.com/gh/pangeo-data/pangeo-binder/tree/staging) | [![Documentation Status](https://readthedocs.org/projects/pangeo-binder/badge/?version=staging)](https://pangeo-binder.readthedocs.io/en/staging/?badge=staging) | https://staging.binder.pangeo.io/
prod | [![CircleCI](https://circleci.com/gh/pangeo-data/pangeo-binder/tree/prod.svg?style=svg)](https://circleci.com/gh/pangeo-data/pangeo-binder/tree/prod) | [![Documentation Status](https://readthedocs.org/projects/pangeo-binder/badge/?version=prod)](https://pangeo-binder.readthedocs.io/en/prod/?badge=prod) | https://binder.pangeo.io/


# About Pangeo's Binder

Much like [mybinder.org](https://mybinder.org), the [Pangeo's](https://pangeo.io/) BinderHub deployment ([binder.pangeo.io](https://binder.pangeo.io/)) allows users to create and share custom computing environments. The main distinction between the two BinderHubs is that Pangeo's BinderHub allows users to perform scalable computations using the dask-kubernetes package.

For more information on the Pangeo project, check out the [online documentation](http://pangeo-binder.readthedocs.io/).

## How to Deploy:
This repo is continuously deployed using [CircleCI](https://circleci.com/gh/pangeo-data/pangeo-binder). It can also be deployed from a local computer using the following command:
```
cd helm-chart
deployment={staging,prod}  # choose one
helm upgrade --wait --install --namespace=${deployment} ${deployment} \
    pangeo-binder --version=v0.2.0 \
    -f ../deploy/${deployment}.yaml \
    -f ../secrets/${deployment}.yaml
```

## More Information

The setup and configuration of Pangeo's BinderHub largely follows the [Zero to Binderhub](https://binderhub.readthedocs.io/en/latest/) instructions. A few key distinctions are present:

1. We define our own chart, [pangeo-binder](https://github.com/pangeo-data/pangeo-binder/tree/staging/helm-chart/pangeo-binder), so that we can mix in some Pangeo spccific bits (e.g. a RBAC for dask-kubernetes). The pangeo-binder chart is based on the binderhub chart but most settings are indented under the `binderhub` chart level. The mybinder.org project does the same thing in [mybinder.org-deploy](https://github.com/jupyterhub/mybinder.org-deploy).
2. The deployment steps in [section 3.4 of the Zero to Binderhub documentation](https://binderhub.readthedocs.io/en/latest/setup-binderhub.html#install-binderhub) are modified slightly to account for the pangeo-binder chart. The steps are briefly outlined below:
    ```
    # get current versions of the chart dependencies
    cd helm-chart/pangeo-binder
    helm dependency update

    # install the pangeo-binder chart
    helm install pangeo-binder --version=0.2.0-...  --name=<choose-name> --namespace=<choose-namespace> -f secret.yaml -f config.yaml
    ```

## Additional Links and Related Projects

- Pangeo Project: http://pangeo.io/
- Pangeo-Binder Issue Tracker: https://github.com/pangeo-data/pangeo-binder/issues
- Zero to BinderHub Documentation: https://binderhub.readthedocs.io/en/latest/
- MyBinder Documentation: https://mybinder.readthedocs.io/en/latest/
