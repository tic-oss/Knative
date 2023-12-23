## Service To Service Eventing via Kafka Broker

### Pre-requisites

1. Knative 
2. Kafka cluster 
3. Kafka Broker

### Deploy Backend as Knative Service

- Deploy the backend as knative service using:
```
kubectl apply -f backend.yml
```

- Create a Sink binding between the backend service and the kafka broker using:
```
kubectl apply -f backend-sinkbinding.yml
```

- Create a self subscription(trigger) between the backend service and the kafka broker so that i will receive it's own events from kafka broker using:
```
kubectl apply -f backend-self-trigger.yml
```

- or else, simply apply all the manifest files at once using:
```
kubectl apply -f .
```

### How to check service-service eventing flow ?

- Hit the POST URL: `/kafka-broker` which will send the dummy cloud event to the kafka broker.
- Now Beacuse of the Trigger Configured, the same cloud event will be sent back to the backend service on the `/` endpoint.
- Below are the logs generated:
    1. Red box: sending cloud event.
    2. Yellow box: receiving cloud event.

![Alt text](https://i.imgur.com/ZmFshMX.png)

### How destory the created resources ?

- Destory all the knative components using: 
```
kubectl delete -f . 
```

