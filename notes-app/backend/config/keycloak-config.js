require('dotenv').config();

var keycloakConfig = {
    clientId: 'web_app',
    bearerOnly: true,
    serverUrl: process.env.KC_HOST,
    realm: 'jhipster',
};

module.exports = {
    keycloakConfig,
};
