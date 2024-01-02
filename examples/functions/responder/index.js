const https = require('https');
const http = require('http');
const { CloudEvent } = require('cloudevents');

const sendDataToAPI = async (url, data) => {
  const options = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    }
  };

  const client = url.startsWith('https') ? require('https') : require('http'); // Assuming you've missed the require statements for http and https

  return new Promise((resolve, reject) => {
    const req = client.request(url, options, (res) => {
      res.setEncoding('utf8');
      let responseBody = '';

      res.on('data', (chunk) => {
        responseBody += chunk;
      });

      res.on('end', () => {
        if (res.statusCode === 200) {
          console.log(`Data was sent to ${url}, data: ${JSON.stringify(data)}`);
          resolve();
        } else {
          reject(new Error(`Failed to send data to API, status code: ${res.statusCode}, response: ${responseBody}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.write(JSON.stringify(data));
    req.end();
  });
};

const handle = async (context, event) => {
  console.log(`----------------Logging received Cloud Event------------------`);
  console.log(event);

  const backendApiUri = process.env.REACT_APP_BACKEND_URI || 'http://example-backend.default.10.98.165.95.sslip.io';

  switch (event.type) {
    case 'components':
      try {
        await sendDataToAPI(`${backendApiUri}/receiver`, event.data);
      } catch (error) {
        context.log.error(error);
        throw error;
      }
      break;
    // Add more cases to send the data to different soruces
    default:
      console.log(`Unknown event type: ${event.type}`);
  }
  
  return {
    statusCode: 200,
    body: undefined  // or use null if necessary
  };
};

module.exports = { handle };
