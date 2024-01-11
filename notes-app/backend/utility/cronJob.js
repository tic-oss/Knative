const cron = require("node-cron");
const { httpTransport, emitterFor, CloudEvent } = require("cloudevents");

// Get Knative Broker URI from SinkBinding
// K_SINK env will be automatically populated once the SinkBinding is available
const KnativeEventingBrokerUri =
  process.env.K_SINK ||
  "http://kafka-broker-ingress.knative-eventing.svc.cluster.local/default/kafka-broker";

const cronJob = () => {
  cron.schedule("*/10 * * * * *", async () => {
    console.log("Cron job running every 10 seconds");
    console.log("broker uri:", KnativeEventingBrokerUri);
    try {
      // dummy data [dummy cloud event]
      const ce = new CloudEvent({
        type: "Trigger",
        source: "backend",
        data: {},
      });
      const emit = emitterFor(httpTransport(KnativeEventingBrokerUri));
      // Emit the CloudEvent to the target URL
      emit(ce)
        .then((response) => {
          console.log(`CloudEvent emitted!`, response);
        })
        .catch((error) => {
          console.error("Error sending CloudEvent:", error);
        });
    } catch (error) {
      // Handle errors, if any
      console.error("Error sending dummy cloud event:", error.message);
    }
  });
};

module.exports = cronJob;
