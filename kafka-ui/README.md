## Deploy Kafka UI (provectus) on Kubernetes

### Pre-requisites:
 
1. helm
2. Kafka cluster deployed on Kubernetes

 NOTE: If you need to set up a Kafka cluster, you can do this by following the instructions on the Strimzi Quickstart page(https://strimzi.io/quickstarts/).

### Deploy Kafka UI

1. Create a configMap for the kafka UI.

 NOTE: This configuration will only work if you have deployed the kafka cluster using Strimzi Quickstart page(https://strimzi.io/quickstarts/), else make sure you change the `bootstrapServers: my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092` accordingly in configMap before applying.

```
kubectl apply -f configMap.yml
```

2. Clone/Copy helm Chart to your working directory

```
helm repo add kafka-ui https://provectus.github.io/kafka-ui-charts
```

4. Install the Kafka UI using helm

```
helm install kafka-ui kafka-ui/kafka-ui --set yamlApplicationConfigConfigMap.name="kafka-ui-configmap",yamlApplicationConfigConfigMap.keyName="config.yml"
```

3. Access the Kafka(provectus) UI using:

```
kubectl port-forward service/kafka-ui 8080:80
```

### How destory the created resources ?

- Destory the kafka-ui using: 

```
helm uninstall kafka-ui 
```

### References:

1. https://docs.kafka-ui.provectus.io/configuration/helm-charts/quick-start