curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash 
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig ~/.kube/config