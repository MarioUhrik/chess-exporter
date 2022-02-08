.PHONY: docker
docker:
	docker build -t mariouhrik/chess-exporter:latest .
	docker push mariouhrik/chess-exporter:latest

.PHONY: minikube-deploy
minikube-deploy:
	minikube start
	helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
	helm upgrade -i kube-prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring --create-namespace
	kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
	kubectl apply -k manifests

	@echo "-----------------------TEST ENVIRONMENT SETUP COMPLETED SUCCESSFULLY----------------------------"
	@echo "You can the following command:"
	@echo ""
	@echo "              kubectl -n monitoring port-forward svc/prometheus-operated 9090:9090"
	@echo ""
	@echo "Afterwards, you can use your web browser and visit Prometheus at localhost:9090"

.PHONY: minikube-teardown
minikube-teardown:
	minikube delete
