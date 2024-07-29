# Monitioning

This directory contains  deployments of various addons that integrate with Istio. While these applications are not a part of Istio, they are essential to making the most of Istio's observability features.

## Prerequisites for EKS
---
1. You have created an Amazon EKS cluster.
2. You are using a kubectl client that is configured to communicate with your Amazon EKS cluster.

## Prerequisites for AKS
---
1. You have created an Azure AKS cluster.
2. You are using a kubectl client that is configured to communicate with your Azure AKS cluster.
## Prometheus
---
Prometheus is an open source monitoring system and time series database. You can use Prometheus with Istio to record metrics that track the health of Istio and of applications within the service mesh. You can visualize metrics using tools like Grafana and Kiali.

#### How to access the Prometheus dashboard?
```
kubectl port-forward service/prometheus 9090:9090 -n istio-system
```

## Grafana
---
Grafana is an open source monitoring solution that can be used to configure dashboards for Istio. You can use Grafana to monitor the health of Istio and of applications within the service mesh.

This sample provides the following dashboards:

1. Mesh Dashboard provides an overview of all services in the mesh.

2. Service Dashboard provides a detailed breakdown of metrics for a service.

3. Workload Dashboard provides a detailed breakdown of metrics for a workload.

4. Performance Dashboard monitors the resource usage of the mesh.

5. Control Plane Dashboard monitors the health and performance of the control plane.

6. WASM Extension Dashboard provides an overview of mesh wide WebAssembly extension runtime and loading state.

#### How to access the Grafana dashboard?
```
kubectl port-forward service/grafana 3000:3000 -n istio-system 
```

## Kiali
---
Kiali is an observability console for Istio with service mesh configuration capabilities. It helps you to understand the structure of your service mesh by inferring the topology, and also provides the health of your mesh. Kiali provides detailed metrics, and a basic Grafana integration is available for advanced queries. Distributed tracing is provided by integrating Jaeger.

#### How to access the Kiali dashboard?
```
kubectl port-forward service/kiali 5000:20001 -n istio-system
```
#### NOTE :- 

Add a namespace label to instruct Istio to automatically inject Envoy sidecar proxies when you deploy your application later:

(by default this will be enabled for you, based on the namespace you created for application development, or else you can config it like this:)
```
kubectl label namespace <namespace> istio-injection=enabled
```

kubectl label namespace default istio-injection=enabled --overwrite=true