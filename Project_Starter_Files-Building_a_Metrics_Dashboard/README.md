**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*TODO:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

## Setup the Jaeger and Prometheus source
*TODO:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.

## Create a Basic Dashboard
*TODO:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.

## Describe SLO/SLI
*TODO:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.
99% of all HTTP statuses will be 20x in a given month (Uptime)
99% of all requests will take less than 20ms in a given month (Latency)


## Creating SLI metrics.
*TODO:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 

## Create a Dashboard to measure our SLIs
*TODO:* Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.

## Tracing our Flask App
*TODO:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here.

## Jaeger in Dashboards
*TODO:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.

## Report Error
*TODO:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue.

TROUBLE TICKET

Name:

Date:

Subject:

Affected Area:

Severity:

Description:


## Creating SLIs and SLOs
*TODO:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name three SLIs that you would use to measure the success of this SLO.

## Building KPIs for our plan
*TODO*: Now that we have our SLIs and SLOs, create KPIs to accurately measure these metrics. We will make a dashboard for this, but first write them down here.

## Final Dashboard
*TODO*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  

## References:
https://github.com/opentracing/specification/blob/master/semantic_conventions.md
```
kubectl apply -n observability -f - <<EOF
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: simplest
EOF
``` 
per https://github.com/jaegertracing/jaeger-operator#getting-started
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.0.3/deploy/static/provider/cloud/deploy.yaml`
`kubectl port-forward -n observability  service/simplest-query --address 0.0.0.0 16686:16686`
```
kubectl apply -n observability -f - <<EOF
apiVersion: jaegertracing.io/v1
kind: Jaeger
metadata:
  name: hotrod
EOF
```
`kubectl port-forward -n observability  seßkubectl port-forward -n observability  service/hotrod-query --address 0.0.0.0 16685:16685`
```
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: hotrod
  labels:
    app: hotrod
spec:
  ports:
    - port: 8080
  selector:
    app: hotrod
    tier: frontend
  type: LoadBalancer
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hotrod
  labels:
    app: hotrod
spec:
  selector:
    matchLabels:
      app: hotrod
      tier: frontend
  template:
    metadata:
      labels:
        app: hotrod
        tier: frontend      
    spec:
      containers:
      - image: jaegertracing/example-hotrod:latest
        name: hotrod
        env:
        - name: JAEGER_AGENT_HOST
          value: jaeger
        - name: JAEGER_AGENT_PORT
          value: '6831'
        ports:
        - containerPort: 8080
          name: hotrod
EOF
```
https://www.digitalocean.com/community/tutorials/how-to-implement-distributed-tracing-with-jaeger-on-kubernetes
https://opentracing.io/guides/python/quickstart/
sudo cat /etc/rancher/k3s/k3s.yaml
had to `vagrant destroy` and `conda deactivate` at Exercise_Starter_Files/ first. 
`curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash`
`kubectl create namespace monitoring`
`helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`
`helm repo add stable https://charts.helm.sh/stable`
`helm repo update`
`helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml`
kubectl get pods,svc --namespace=monitoring
kubectl port-forward service/prometheus-grafana --address 0.0.0.0 3000:80 -n monitoring
password: prom-operator
install jaeger per: https://www.jaegertracing.io/docs/1.28/operator/ :
```
kubectl create namespace observability # <1>
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/crds/jaegertracing.io_jaegers_crd.yaml 
`kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/cluster_role.yaml`
`kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/cluster_role_binding.yaml`
`kubectl get deployment jaeger-operator -n observability`
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/service_account.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/role.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/role_binding.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/operator.yaml

```
kubectl get deployments jaeger-operator -n observability
kubectl get pods,svc -n observability

"Shift Command 5" to capture: Photo to view, then: export .png to project folder

`kubectl --namespace monitoring port-forward svc/prometheus-grafana --address 0.0.0.0 5000:80`

