Pangeo Binderhub
================

This repo includes a rough draft of a Pangeo Binderhub.

More details coming soon.

How to deploy:
```
cd helm-chart
helm upgrade prod --install pangeo-binder --namespace=pangeo-binder --version=v0.1.0 -f ../deploy/common.yaml -f ../deploy/prod.yaml -f ../secrets/prod.yaml
```

How to deploy staging:
```
cd helm-chart
helm upgrade staging --install pangeo-binder --namespace=pangeo-binder --version=v0.1.0 -f ../deploy/common.yaml -f ../deploy/staging.yaml -f ../secrets/staging.yaml
```
