Additional deployment things for hub.binder.pangeo.io


```python
kubectl apply -f deploy/nginx-ingress-staging.yaml 
helm install stable/nginx-ingress --name binderhub-proxy --namespace staging -f deploy/nginx-ingress-staging.yaml
```
