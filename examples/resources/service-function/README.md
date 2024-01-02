## Service To Function Eventing via Kafka Broker

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

- Create a subscription(trigger) between the function and the kafka broker so that it will receive it's events from kafka broker using:
```
kubectl apply -f backend-responder-trigger.yml
```

- or else, simply apply all the manifest files at once using:
```
kubectl apply -f .
```

### How to check service-service eventing flow ?

- Hit the POST URL: `/kafka-broker` which will send the dummy cloud event to the kafka broker.
- Now Beacuse of the Trigger Configured, the same cloud event will be sent back to the responder function.
- And as our function is configured to send a post call back to the same example backend service (`/receiver`).
- Check the log to understand more!

### How destory the created resources ?

- Destory all the knative components using: 
```
kubectl delete -f . 
```

