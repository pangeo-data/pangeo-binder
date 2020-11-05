# Deploy metrics
.PHONY: deploy-aws deploy-gcp


deploy-aws:
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
	kubectl create namespace metrics
	# Prometheus
	helm upgrade --wait --install -n metrics prometheus prometheus-community/prometheus \
		-f prometheus-config.yaml
	# nginx for ingress
	# I think we already have nginx-ingress in the regular deployment?
	# helm upgrade --wait --install -n staging ingress-nginx ingress-nginx/ingress-nginx -f ../../metrics/ingress-config.yaml
	# Grafana
	helm upgrade --wait --install -n metrics grafana grafana/grafana \
		-f grafana-config.yaml \
		-f grafana-config-aws.yaml \
		-f ../secrets-aws/staging.yaml

deploy-gcp:
	# Prep
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm repo add grafana https://grafana.github.io/helm-charts
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
	kubectl create namespace metrics
	# Prometheus
	helm upgrade --wait --install -n metrics prometheus prometheus-community/prometheus \
		-f prometheus-config.yaml
	# nginx for ingress
	# I think we already have nginx-ingress in the regular deployment?
	# helm upgrade --wait --install -n staging ingress-nginx ingress-nginx/ingress-nginx -f ../../metrics/ingress-config.yaml
	# Grafana
	helm upgrade --wait --install -n metrics grafana grafana/grafana \
		-f grafana-config.yaml \
		-f grafana-config-gcp.yaml \
		-f ../secrets/staging.yaml
