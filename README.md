Pangeo Binderhub
================

This repo includes a rough draft of a Pangeo Binderhub.

More details coming soon.

How to deploy:
```
cd helm-chart
helm upgrade --wait --install --namespace=prod prod pangeo-binder --version=v0.2.0 -f ../deploy/prod.yaml -f ../secrets/prod.yaml
```

How to deploy staging:
```
cd helm-chart
helm upgrade --wait --install --namespace=staging staging pangeo-binder --version=v0.2.0 -f ../deploy/staging.yaml -f ../secrets/staging.yaml
```
