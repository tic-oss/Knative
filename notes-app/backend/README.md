
### Before starting an application create an .env file and copy paste the below content 

```
DB_URI=mongodb://localhost:27017/
MONGODB_DATABASE=notes-db
KC_HOST=http://localhost:9080
SERVER_PORT=3001
FRONTEND_URL=http://localhost:3000
FUNC_PROCESSOR_URL=http://localhost:8080
```


### Start Application

```
node app.js
```

### Start Services

1. keycloak
2. mongodb

```
 npm run services:up  
```

NOTE: Stop the conatiner manually and restart the same container to persist the data.

