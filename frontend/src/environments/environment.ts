/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'coffeeplace-app.us', // the auth0 domain prefix
    audience: 'coffeeplace', // the audience set for the auth0 app
    clientId: 'gtg3brYpp6D1X8QbIQEm47l1bjouRK5o', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
