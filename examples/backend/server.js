const express = require('express');
var app = express();
const cors = require('cors');

app.use(cors());


const { httpTransport, emitterFor, CloudEvent } = require("cloudevents");
const { isValidType } = require('cloudevents/dist/event/validation');

// Get Knative Broker URI from SinkBinding
// K_SINK env will be automatically populated once the SinkBinding is available
const KnativeEventingBrokerUri = process.env.K_SINK || 'http://broker-ingress.knative-eventing.svc.cluster.local/demo/default';

app.use(express.json());
//app.options('*', cors()); // Enable pre-flight requests for all routes
app.use(cors());
//app.use(cors({origin: '*'}));


// API endpoint for receiving data
app.post('/receiver', (req, res) => {
  // Parse the data from the request
  const incomingData = req.body;
  console.log(`Received data!`);

  // Checking if the incoming data is valid
  if (incomingData && typeof incomingData === 'object') {
    console.log(`----------------Logging received data------------------`);
    console.log(incomingData);
    res.sendStatus(200);
  } else {
    res.sendStatus(400);
  }
});

// API endpoint for receiving data [json, cloudevent] from broker [kafka-broker]
app.post('/', (req, res) => {
  // Add your event processing logic here
  const cloudEventData = req.body;
  console.log(`----------------Logging request headers------------------`);
  console.log('Request Headers:', req.headers);

  console.log(`----------------Logging request body------------------`);
  console.log('Received CloudEvent Data:', cloudEventData);
  res.status(200).send('Event received successfully');
});


// API endpoint to check if backend service is available, this returns http response OK!
app.get('/test', (req, res) => {
  res.sendStatus(200);
});

// API endpoint to send event to the available broker [kafka]
app.post('/kafka-broker', (req, res) => {
  console.log(`----------------Logging Broker URL------------------`);
  console.log("BROKER URL: ", KnativeEventingBrokerUri);

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

  const emit = emitterFor(httpTransport(KnativeEventingBrokerUri));
  // Emit the CloudEvent to the target URL
  emit(ce)
  .then(response => {
    console.log(`CloudEvent emitted!`);
  })
  .catch(error => {
    console.error('Error sending CloudEvent:', error);
  });
  res.sendStatus(200);
});

// Start the server
const port = process.env.PORT || 3333;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});

// signal interrupt
process.on('SIGINT', () => {
  process.exit(0);
});

// event listener for the 'uncaughtException' event
process.on('uncaughtException', err => {
  console.error('Uncaught Exception:', err);
});