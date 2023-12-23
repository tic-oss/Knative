## Example Backend

This example is to show case the  how knative services work with knative broker [inmemory, kafka].

### API Endpoints

- `/test`, this API endpoint to check if backend service is available, this returns http response OK!

- `/receiver`, this API endpoint is for receiving data from any source.

- `/kafka-broker`, this API endpoint is to send cloud event to the available broker [kafka], it send a dummy cloud event with ce-type: "components"

```
  // dummy data [dummy cloud event]
  const ce = new CloudEvent({
    type: 'components',
    source: 'backend',
    data: {
      serving: 'knative-serving',
      eventing: 'knative-eventing',
      orchestration: 'kubernetes',
      broker: 'kafka',
      backend: 'node',
      framework: 'express',
    }
  });
```

- `/`, this API endpoint is for receiving data [json, cloudevent] from broker [kafka-broker].

### Running the backend application in local 

1. For the first time install node modules using: `npm install`
2. Start the backend application using: `node server.js`

### Running the backend application using docker 

1. Build a docker image using: `docker build cmd`.

```
docker build -t raxkumar/knative-example-backend .
```
2. Run the image using: `docker run cmd`.

```
docker run -p3333:3333 raxkumar/knative-example-backend 
```