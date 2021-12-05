**Note:** For the screenshots, you can store all of your answer images in the `answer-img` directory.

## Verify the monitoring installation

*TODO1:* run `kubectl` command to show the running pods and services for all components. Take a screenshot of the output and include it here to verify the installation

## Setup the Jaeger and Prometheus source
*TODO2:* Expose Grafana to the internet and then setup Prometheus as a data source. Provide a screenshot of the home page after logging into Grafana.

## Create a Basic Dashboard
*TODO3:* Create a dashboard in Grafana that shows Prometheus as a source. Take a screenshot and include it here.

## Describe SLO/SLI
*TODO4:* Describe, in your own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time*.
If the SLO is "99% monthly Uptime", then the SLI could be the measurement of "proportion HTTP requests that return with 2XX and 3XX status". 
If the SLO is "99% of all requests will take less than 20ms in a given month (Latency)", then an SLI can be expressed as the "percentage of requests successfully retrieving before 20ms over the past month".

*TODO5:* It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs. 
5.1 traffic: We want to know how often our customers are visiting our application. With that in mind, we can have an SLI of "per-second average requests over the last hour for the past 4 weeks"; the metric can be : `rate(http_requests_total[1h])[4w:10m]`
5.2 latency: We want our customers to have reasonable response time on our applications. With that in mind, we can have an SLI of "average request duration during the last 5 minutes"; the metric can be: `rate(prometheus_http_request_duration_seconds_sum[5m])/rate(prometheus_http_request_duration_seconds_count[5m])`
5.3  latency: If the SLO is "99% of all requests will take less than 20ms in a given month (Latency)", then an SLI can be expressed as the "percentage of requests successfully retrieving before 20ms over the past month"; metric can be: `sum(rate(prometheus_http_request_duration_seconds_bucket{le="0.02"}[5m])) by (job)/  sum(rate(prometheus_http_request_duration_seconds_count[5m])) by (job)`
so that we can alert when the ratio goes below 99%, or 
5.4 latency(continue from 5.3): given the same SLO as in 5.3, another SLI could be the 95th percentile, i.e. "the request duration within which 95% of all requests fall"; the metric could be:
`histogram_quantile(0.95, sum(rate(prometheus_http_request_duration_seconds_bucket[5m])) by (le))`
5.5 error: We want our application working most if not all of the time for our customers.  An SLI can be "percentage of non 2xx response status code"; the metric can be: `http_requests_total{status!~"20."}/http_requests_total` ; or "percentage of 2xx and 3xx response status code"; the metric: `sum(prometheus_http_requests_total{code=~"2.*|3.*", job="xxx"})/sum(prometheus_http_requests_total{job="xxx"})`

5.6 saturation: //unused memory in MiB for every instance (on a fictional cluster scheduler exposing these metrics about the instances it runs):
`(instance_memory_limit_bytes - instance_memory_usage_bytes) / 1024 / 1024` 
//the top 3 CPU users grouped by application (app) and process type (proc) like this:
`topk(3, sum by (app, proc) (rate(instance_cpu_time_ns[5m])))`
5.7 availability: We want our app to be available to our customers most of the time. The SLI can "the app returns for 99.995% of the time"; metric: `sum(prometheus_http_requests_total{code=~"2.*|3.*|4..", job="xxx"})/sum(prometheus_http_requests_total{job="xxx"})`

## Create a Dashboard to measure our SLIs
*TODO6:* Create a dashboard to measure the uptime of the frontend and backend services. We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.
http_requests_total{status!~"20."}
http_requests_total{status~"40."}
http_requests_total{status~"50."}

## Tracing our Flask App
*TODO7:*  We will create a Jaeger span to measure the processes on the backend. Once you fill in the span, provide a screenshot of it here.

## Jaeger in Dashboards
*TODO8:* Now that the trace is running, let's add the metric to our current Grafana dashboard. Once this is completed, provide a screenshot of it here.

## Report Error
*TODO9:* Using the template below, write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue.


Name:

Date:

Subject:

Affected Area:

Severity:

Description:


## Creating SLIs and SLOs
*TODO10:* We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name three SLIs that you would use to measure the success of this SLO.

## Building KPIs for our plan
*TODO11*: Now that we have our SLIs and SLOs, create KPIs to accurately measure these metrics. We will make a dashboard for this, but first write them down here.

## Final Dashboard
*TODO12*: Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs. Include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  

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
`kubectl port-forward -n observability  service/hotrod-query --address 0.0.0.0 16685:16685`
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
`sudo cat /etc/rancher/k3s/k3s.yaml`; in vi: gg, d then G: paste
[had to `vagrant destroy` and `conda deactivate` at Exercise_Starter_Files/ first; had to `vagrant destroy` at parent folder `Project_Starter_Files-Building_a_Metrics_Dashboard` first.]
% kubectl get node -o wide
kubectl describe node localhost
kubect exec -it metrics-server-7b4f8b595-jjxzv -n kube-system -- bash //error "container_linux.go:370:"
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash //helm installed into /usr/local/bin/helm
`kubectl create namespace monitoring`
`helm repo add prometheus-community https://prometheus-community.github.io/helm-charts` //"prometheus-community" has been added to your repositories
`helm repo add stable https://charts.helm.sh/stable` //"stable" has been added to your repositories
`helm repo update` //Update Complete. ⎈Happy Helming!⎈
`helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml`//no such file or directory
`helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig ~/.kube/config`//kube-prometheus-stack has been installed. Check its status by running:
//  kubectl --namespace monitoring get pods -l "release=prometheus"
//Visit https://github.com/prometheus-operator/kube-prometheus for instructions on how to create & configure Alertmanager and Prometheus instances using the Operator.
kubectl get pods,svc --namespace=monitoring
% kubectl get pods,svc -n monitoring //see TODO1
`kubectl port-forward service/prometheus-grafana --address 0.0.0.0 3000:80 -n monitoring` # address already in use, so had to:
`kubectl port-forward service/prometheus-grafana --address 0.0.0.0 5000:80 -n monitoring` 
# Forwarding from 0.0.0.0:5000 -> 3000

password: prom-operator
install jaeger per: https://www.jaegertracing.io/docs/1.28/operator/ :
```
kubectl create namespace observability 
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/crds/jaegertracing.io_jaegers_crd.yaml 
`kubectl get deployment jaeger-operator -n observability`
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/service_account.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/role.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/role_binding.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/operator.yaml

kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/cluster_role.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/cluster_role_binding.yaml

```
`kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role.yaml`
kubectl get deployments jaeger-operator -n observability
kubectl get pods,svc -n observability

"Shift Command 5" to capture: Photo to view, then: export .png to project folder

`kubectl --namespace monitoring port-forward svc/prometheus-grafana --address 0.0.0.0 5000:80` #
`% kubectl apply -f manifests/my-trace-jaeger-instance.yaml`
`manifests % kubectl get svc -n observability` # see svc/my-trace-query and another 3 my-trace-* services
`my-trace-query.default.svc.cluster.local:16686` as data source: # Jaeger: Bad Gateway. 502. Bad Gateway
 should be `my-trace-query.observability.svc.cluster.local:16686`
 `kubectl port-forward -n observability  service/my-trace-query --address 0.0.0.0 16686:16686` # localhost:16686 for jaeger

`(backend_env) <my-mac> backend % docker tag star-backend:latest treefishdocker/star-backend:latest`
`(backend_env)  app % kubectl apply -f backend-deployment.yaml -n default`
How does Prometheus know this flask app wants to be monitored? https://github.com/rycus86/prometheus_flask_exporter
`vagrant@localhost:~> kubectl get all --all-namespaces`
` k8s % kubectl get jaeger`
`kubectl port-forward $(kubectl get pods -l=app="my-sample-app" -o name) 8888:8888`
`for in in 1, 2, 3; do curl localhost:8888; done`
https://access.redhat.com/documentation/en-us/openshift_container_platform/4.4/html/jaeger/jaeger-sidecar-automatic_jaeger-deploying
`(base) ~ % kubectl get jaeger -o wide --all-namespaces`
jaeger strategy: https://access.redhat.com/documentation/en-us/openshift_container_platform/4.7/html/jaeger/jaeger-installation
` manifests % kubectl delete --all pods --namespace=default --grace-period=0 --force` 
or: https://stackoverflow.com/questions/33509194/command-to-delete-all-pods-in-all-kubernetes-namespaces
`manifests % kubectl apply -f app/ -n default`
`(base) mommy@Mommys-iMac ~ % kubectl get ingress -n observability`
## Debug
Error on `vagrant up`: "...because the filesystem "vboxsf" is not available. This filesystem is..": 
At where Vagrantfile is : `vagrant plugin install vagrant-vbguest` per https://stackoverflow.com/questions/43492322/vagrant-was-unable-to-mount-virtualbox-shared-folders
data source for jaeger at Grafana: either `localhost:16686` or `my-trace-query.observability.svc.cluster.local:16686`
https://stackoverflow.com/questions/64445937/prometheus-monitor-all-services-without-creating-servicemonitor-for-each-servic
(udaconnect_env) c manifests % kubectl port-forward   service/backend-service --address 0.0.0.0 8083:8081 # backend-service 200
5001: grafana
16686: jaeger
kubectl describe servicemonitor prometheus-kube-prometheus-coredns -n monitoring
(backend_env)  backend % docker tag backend:latest treefishdocker/backend.latest
(backend_env)  manifests % kubectl edit servicemonitor common-monitor -n monitoring
https://support.coreos.com/hc/en-us/articles/360000155514-Prometheus-ServiceMonitor-troubleshooting
https://stackoverflow.com/questions/52991038/how-to-create-a-servicemonitor-for-prometheus-operator
https://rancher.com/docs/rancher/v2.5/en/monitoring-alerting/how-monitoring-works/
https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/api.md#servicemonitor
targetPort: Name or number of the target port of the Pod behind the Service, the port must be specified with container port property. Mutually exclusive with port.	
Finally, request received to the service’s port, and forwarded on the targetPort of the pod.
#### to delete pods by parts of name
 kubectl get pods -n default --no-headers=true | awk '/frontend|backend/{print $1}'| xargs  kubectl delete -n default pod --grace-period=0 --force
 per https://stackoverflow.com/questions/59473707/kubenetes-pod-delete-with-pattern-match-or-wilcard
   
kubectl get prometheus -o yaml -n monitoring 
# with         release: prometheus prometheus grabs service monitors; with monitoring: true sm gets svcs. 

click at 8082 : net::ERR_NAME_NOT_RESOLVED; err backend.default.svc.cluster.local: https://knowledge.udacity.com/questions/741234
kubectl get -n observability ingress -o yaml | tail #       servicePort: 16686
per https://blog.mphomphego.co.za/blog/2021/07/25/How-to-configure-Jaeger-Data-source-on-Grafana-and-debug-network-issues-with-Bind-utilities.html
ingress_name=$(
  kubectl get -n observablity ingress -o jsonpath='{.items[0].metadata.name}'
  )
  ; \
ingress_port=$(
  kubectl get -n observability ingress -o jsonpath='{.items[0].spec.defaultBackend.service.port.number}'
  )
  ; \
echo -e "\n\n${ingress_name}.${namespace}.svc.cluster.local:${ingress_port}"
kubectl -n observability get pod jaeger-operator-7bb8f65994-6zj22 -oyaml | grep -A 4 WATCH_NAMESPACE
https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/
https://www.jaegertracing.io/docs/1.28/operator/: "download and customize the operator.yaml, setting the env var WATCH_NAMESPACE to have an empty value, so that it can watch for instances across all namespaces" to `        - start
        env:
        - name: WATCH_NAMESPACE
          value: ""`
          (udaconnect_env)  CNAND_nd064_C4_Observability_Starter_Files % kubectl edit deploy jaeger-operator -n observability
Project_Starter_Files-Building_a_Metrics_Dashboard % kubectl port-forward service/prometheus-grafana --address 0.0.0.0 5000:80 -n monitoring
          (udaconnect_env)  CNAND_nd064_C4_Observability_Starter_Files %  kubectl port-forward -n observability  service/my-trace-query --address 0.0.0.0 16686:16686
          (udaconnect_env) CNAND_nd064_C4_Observability_Starter_Files % kubectl port-forward  service/frontend-service 8082                  
          (udaconnect_env)  Project_Starter_Files-Building_a_Metrics_Dashboard % kubectl apply -f manifests/jaeger-role-binding-for-default.yaml

          rate(flask_http_request_total[5m])? is 0?

          kubectl delete all --all -n {my-namespace}
          
          
          (udaconnect_env) mommy@Mommys-iMac manifests % kubectl get ns observability -o json > tmp.json
          edit tmp.json so that: `"finalizers": []`
                    `kubectl proxy`
`curl -k -H "Content-Type: application/json" -X PUT --data-binary @tmp.json http://127.0.0.1:8001/api/v1/namespaces/developer/finalize <new tmp.json>`
           kubectl port-forward  service/backend 8081 -n observability     
          kubectl port-forward -n observability  service/my-trace-query --address 0.0.0.0 16686:16686
          kubectl port-forward service/prometheus-grafana --address 0.0.0.0 5000:80 -n monitoring
Tip#1: only one vagrant on your local machine
Fix when seeing on "vagrant up": https://blog.mphomphego.co.za/blog/2021/01/14/A-VirtualBox-machine-with-the-name-already-exists/html
`BAD_VM='master'`                                               
`VM_ID=$(vboxmanage list vms | grep ${BAD_VM} | cut -f 2 -d ' ')`
`vboxmanage unregistervm ${VM_ID} --delete`
AND: `vagrant global-status --prune` then `vagrant destroy xxxx`
update vb version per:        
Error: "mount: /vagrant: unknown filesystem type 'vboxsf'.": https://knowledge.udacity.com/questions/711201
Error: error: Pod 'backend-68bd676ccd-trxj4' does not have a named port 'backendport' //this is a terminating pod?!