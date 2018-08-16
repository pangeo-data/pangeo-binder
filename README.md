Pangeo Binderhub
================

This repo includes a rough draft of a Pangeo Binderhub.

More details coming soon.

How to deploy:
```
cd helm-chart
helm upgrade binder --install pangeo-binder --namespace=pangeo-binder --version=v0.1.0 -f ../deploy/binder_config.yml -f ../deploy/mybinder_secret.yaml
```
