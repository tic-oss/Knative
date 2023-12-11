# Python HTTP Function

Welcome to your new Python function project! The boilerplate function
code can be found in [`func.py`](./func.py). This function will respond
to incoming HTTP GET and POST requests.

## Endpoints

Running this function will expose three endpoints.

  * `/` The endpoint for your function.
  * `/health/readiness` The endpoint for a readiness health check
  * `/health/liveness` The endpoint for a liveness health check

The health checks can be accessed in your browser at
[http://localhost:8080/health/readiness]() and
[http://localhost:8080/health/liveness]().

You can use `func invoke` to send an HTTP request to the function endpoint.


## Testing

This function project includes a [unit test](./test_func.py). Update this
as you add business logic to your function in order to test its behavior.

```console
python test_func.py
```
## HOW TO RUN IT LOCALLY ?

Run the below command to create a virtual env.
```
virtualenv venv --python=python3
```

Run the below command to install the requirements.
```
pip3 install -r requirements.txt
```

Run the function using below cmd:

```
python3 func.py 
```