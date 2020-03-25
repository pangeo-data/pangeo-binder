# Deploy k8s cluster on aws eks


##### Deploy cluster and nodegroups
```
eksctl create cluster -f eksctl-config.yml
```


##### Patch default aws-storage class (https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/1413)
```
kubectl apply -f storage-class.yml
kubectl patch storageclass gp2 -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
```


##### Deploy cluster autoscaler
```
kubectl apply -f cluster-autoscaler.yml
```


##### Deploy binderhub
```
export CIRCLE_BRANCH=staging
kubectl create namespace $CIRCLE_BRANCH
helm upgrade --wait --install ${CIRCLE_BRANCH} pangeo-binder --namespace=${CIRCLE_BRANCH} --version=v0.2.0 -f ./deploy-aws/${CIRCLE_BRANCH}-install.yaml -f ./secrets-aws/${CIRCLE_BRANCH}-install.yaml --cleanup-on-fail
```
NOTE: confirm non-https deployment working by `kubectl get pods -A` and going to external-ip from `kubectl get svc binder -n $CIRCLE_BRANCH`


##### Upgrade binderhub w/ manually edited https settings
NOTE: add loadbalanerIPs to secrets-aws/staging.yaml, update DNS settings for domain name
```
export CIRCLE_BRANCH=staging
helm upgrade --wait --install ${CIRCLE_BRANCH} pangeo-binder --namespace=${CIRCLE_BRANCH} --version=v0.2.0 -f ./deploy-aws/${CIRCLE_BRANCH}.yaml -f ./secrets-aws/${CIRCLE_BRANCH}.yaml --cleanup-on-fail
```


##### Set up HTTPS (https://binderhub.readthedocs.io/en/latest/https.html)
NOTE: edit binderhub-issuer-staging.yaml with your email
```
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v0.11.0/cert-manager.yaml --validate=false
# Wait about 2 minutes for 'webhook' to start running before running this command:
kubectl apply -f binderhub-issuer-${CIRCLE_BRANCH}.yaml
```
You should now have a functioning binderhub at https://staging.aws-uswest2-binder.pangeo.io !!!


##### Removing things:
you can get rid of resources created with `kubectl apply` with `kubectl delete`:
```
kubectl delete -f https://github.com/jetstack/cert-manager/releases/download/v0.11.0/cert-manager.yaml
```

Or tear everything down with
```
helm delete staging -n staging
```
