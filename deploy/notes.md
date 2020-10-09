```console
$ kubectl apply -f deploy/nginx-ingress-staging.yaml 
$ helm upgrade --install binderhub-proxy stable/nginx-ingress --namespace staging -f deploy/nginx-ingress-staging.yaml
$ kubectl -n staging delete deployment staging-kube-lego
$ helm upgrade --install ...
```

Fails with

```
Error: UPGRADE FAILED: rendered manifests contain a resource that already exists. Unable to continue with update: Ingress "jupyterhub" in namespace "staging" exists and cannot be imported into the current release: invalid ownership metadata; label validation error: missing key "app.kubernetes.io/managed-by": must be set to "Helm"; annotation validation error: missing key "meta.helm.sh/release-name": must be set to "staging"; annotation validation error: missing key "meta.helm.sh/release-namespace": must be set to "staging"
```

Delete those

```
$ kubectl -n staging delete ingress/binderhub ingress/jupyterhub ingress/kube-lego-nginx
```

Failed with

```
upgrade.go:367: [debug] warning: Upgrade "staging" failed: failed to replace object: PersistentVolumeClaim "hub-db-dir" is invalid: spec: Forbidden: is immutable after creation except resources.requests for bound claims && failed to replace object: Service "hub" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "proxy-api" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "proxy-public" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "binder" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "api-staging-dask-gateway" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "traefik-staging-dask-gateway" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "staging-nginx-ingress-controller" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "staging-nginx-ingress-default-backend" is invalid: spec.clusterIP: Invalid value: "": field is immutable
Error: UPGRADE FAILED: failed to replace object: PersistentVolumeClaim "hub-db-dir" is invalid: spec: Forbidden: is immutable after creation except resources.requests for bound claims && failed to replace object: Service "hub" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "proxy-api" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "proxy-public" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "binder" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "api-staging-dask-gateway" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "traefik-staging-dask-gateway" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "staging-nginx-ingress-controller" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "staging-nginx-ingress-default-backend" is invalid: spec.clusterIP: Invalid value: "": field is immutable
helm.go:94: [debug] failed to replace object: PersistentVolumeClaim "hub-db-dir" is invalid: spec: Forbidden: is immutable after creation except resources.requests for bound claims && failed to replace object: Service "hub" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "proxy-api" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace
object: Service "proxy-public" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "binder" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "api-staging-dask-gateway" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "traefik-staging-dask-gateway" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "staging-nginx-ingress-controller" is invalid: spec.clusterIP: Invalid value: "": field is immutable && failed to replace object: Service "staging-nginx-ingress-default-backend" is invalid: spec.clusterIP: Invalid value: "": field is immutable
```

-----


https://binderhub.readthedocs.io/en/latest/https.html

1. Reserve a static IP through GCP

```console
$ kubectl apply -f deploy/binderhub-issuer-prod.yaml  
issuer.cert-manager.io/letsencrypt-production created

$ helm install binderhub-proxy stable/nginx-ingress --namespace prod -f deploy/nginx-ingress-prod.yaml 
```

-------


```console
helm mapkubeapis -n prod prod
2020/10/09 14:39:34 Release 'prod' will be checked for deprecated or removed Kubernetes APIs and will be updated if necessary to supported API versions.
2020/10/09 14:39:34 Get release 'prod' latest version.
2020/10/09 14:39:35 Check release 'prod' for deprecated or removed APIs...
2020/10/09 14:39:35 Found deprecated or removed Kubernetes API:
"apiVersion: extensions/v1beta1
kind: Deployment"
Supported API equivalent:
"apiVersion: apps/v1
kind: Deployment"
2020/10/09 14:39:35 Found deprecated or removed Kubernetes API:
"apiVersion: extensions/v1beta1
kind: Ingress"
Supported API equivalent:
"apiVersion: networking.k8s.io/v1beta1
kind: Ingress"
2020/10/09 14:39:35 Found deprecated or removed Kubernetes API:
"apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding"
Supported API equivalent:
"apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding"
2020/10/09 14:39:35 The following API does not require mapping as the API is not deprecated or removed in Kubernetes 'v1.17':
"apiVersion: rbac.authorization.k8s.io/v1beta1
kind: ClusterRoleBinding"
2020/10/09 14:39:35 Finished checking release 'prod' for deprecated or removed APIs.
2020/10/09 14:39:35 Deprecated or removed APIs exist, updating release: prod.
2020/10/09 14:39:35 Set status of release version 'prod.v108' to 'superseded'.
2020/10/09 14:39:35 Release version 'prod.v108' updated successfully.
2020/10/09 14:39:35 Add release version 'prod.v109' with updated supported APIs.
2020/10/09 14:39:36 Release version 'prod.v109' added successfully.
2020/10/09 14:39:36 Release 'prod' with deprecated or removed APIs updated successfully to new version.
2020/10/09 14:39:36 Map of release 'prod' deprecated or removed APIs to supported versions, completed successfully.
```
