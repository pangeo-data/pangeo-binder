Pangeo Binderhub
================

This repo includes a rough draft of a Pangeo Binderhub.

More details coming soon.

How to deploy:
```
cd helm-chart
helm upgrade binder --install pangeo-binder --namespace=pangeo-binder --version=v0.1.0 -f ../deploy/binder_config.yml -f ../deploy/mybinder_secret.yaml
```

How to deploy staging:
```
cd helm-chart
helm upgrade binder --install pangeo-binder --namespace=staging --version=v0.1.0 -f ../deploy/staging_config.yml -f ../deploy/staging_secret.yaml
```

Ask @jhamman or @dsludwig for ``mybinder_secret.yaml`` or
``staging_secret.yaml`` to deploy ``binder.pangeo.io`` or
``staging.binder.pangeo.io``.
