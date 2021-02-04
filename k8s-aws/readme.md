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
#curl https://get.helm.sh/helm-v3.1.2-linux-amd64.tar.gz | tar -xzf -
#sudo mv linux-amd64/helm /usr/local/bin
helm version #>3
helm repo add pangeo https://pangeo-data.github.io/helm-chart/
helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo add dask-gateway https://dask.org/dask-gateway-helm-repo/
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://kubernetes-charts.storage.googleapis.com/
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
cd pangeo-binder/pangeo-binder
helm dependency update
cd ../
```

Initial install takes ~ 3mins for everything to be created
```
export CIRCLE_BRANCH=staging
kubectl create namespace $CIRCLE_BRANCH
helm upgrade --wait --install ${CIRCLE_BRANCH} pangeo-binder --namespace=${CIRCLE_BRANCH} --version=v0.2.0 -f ./deploy-aws/${CIRCLE_BRANCH}-install.yaml -f ./secrets-aws/${CIRCLE_BRANCH}-install.yaml --cleanup-on-fail
```
NOTE: confirm non-https deployment working by `kubectl get pods -A` and going to external-ip from `kubectl get svc binder -n $CIRCLE_BRANCH`


##### Set up HTTPS (https://binderhub.readthedocs.io/en/latest/https.html)
NOTE: edit binderhub-issuer-staging.yaml with your email
```
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v0.11.0/cert-manager.yaml --validate=false
# Wait about 2 minutes for 'webhook' to start running before running this command:
kubectl apply -f k8s-aws/binderhub-issuer-${CIRCLE_BRANCH}.yaml
```

##### Upgrade binderhub w/ manually edited https settings

NOTE: add loadbalanerIPs to secrets-aws/staging.yaml, update DNS settings for domain name

Will also need to change various `hosts` in `deploy-aws/staging.yaml` or `deploy-aws/prod.yaml` as well as the same file in `secrets-aws/` if you are not hosting the binderhub through `staging.aws-uswest2-binder.pangeo.io`.

```
export CIRCLE_BRANCH=staging
helm upgrade --wait --install ${CIRCLE_BRANCH} pangeo-binder --namespace=${CIRCLE_BRANCH} --version=v0.2.0 -f ./deploy-aws/${CIRCLE_BRANCH}.yaml -f ./secrets-aws/${CIRCLE_BRANCH}.yaml --cleanup-on-fail
```

Check on deployment history
```
helm list -A
helm history -n staging staging
```

You should now have a functioning binderhub at https://staging.aws-uswest2-binder.pangeo.io !!!

##### link IAM role to pangeo service account
For singleuser notebook pods and dask worker pods
see https://eksctl.io/usage/iamserviceaccounts/
```
eksctl create iamserviceaccount --config-file=k8s-aws/eksctl-config.yml

#Or:
eksctl create iamserviceaccount --region=us-west-2 --cluster=pangeo-binder --namespace=prod --name=pangeo --attach-policy-arn=arn:aws:iam::783380859522:policy/pangeo-data-s3  --profile circleci --override-existing-serviceaccounts --approve
```


##### Removing things:
you can get rid of resources created with `kubectl apply` with `kubectl delete`:
```
kubectl delete -f https://github.com/jetstack/cert-manager/releases/download/v0.11.0/cert-manager.yaml
kubectl delete -f k8s-aws/binderhub-issuer-${CIRCLE_BRANCH}.yaml
```

Tear the binderhub down with
```
helm delete staging -n staging
```

Remove `prometheus-operator` custom resource definitions (CRDs)
```
kubectl delete crd --all
```

Remove DNS settings and records.

Other cheatsheet commands:
```
eksctl delete iamserviceaccount --cluster pangeo-binder --name pangeo --namespace staging
```


## Update Cluster (K8s version and nodegroups)
https://eksctl.io/usage/cluster-upgrade/

last did this 2/3/2021 with eksctl 0.37.0
```
eksctl upgrade cluster --name=pangeo-binder --approve
eksctl utils update-kube-proxy --profile circleci --name pangeo-binder --region us-west-2 --approve
eksctl utils update-aws-node --profile circleci --name pangeo-binder --region us-west-2 --approve
eksctl utils update-coredns --profile circleci --name pangeo-binder --region us-west-2 --approve
```

create new nodegroups
```
eksctl create nodegroup --profile circleci --config-file=eksctl-config.yml
```

bump autoscaler version (1.16.7)
https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler#releases
```
kubectl apply -f cluster-autoscaler.yml
```

Need to upgrade certmanager  https://cert-manager.io/docs/installation/kubernetes/
https://cert-manager.io/docs/installation/uninstall/kubernetes/
```
kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.1.0/cert-manager.yaml
```
and update binderhub-issuer-staging.yaml to use `apiVersion: cert-manager.io/v1`
(https://cert-manager.io/docs/configuration/acme/#creating-a-basic-acme-issuer)
```
# Wait about 2 minutes for 'webhook' to start running before running this command:
kubectl apply -f binderhub-issuer-staging.yaml
```
