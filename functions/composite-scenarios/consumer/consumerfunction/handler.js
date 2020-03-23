'use strict'
const request = require("request");

module.exports = (event, context) => {
  console.log(event);
  console.log(context);
  const gateway_endpoint = process.env.gateway_endpoint;

  if (!gateway) {
      return context.status.fail('Gateway URL is missing')
  }
  let param = 1;
  const isExist = 'param' in event['query'];
  if (isExist) {
      param = event['query']['param']

  }
  // This call to a matrix function
  const url = gateway_endpoint + "/function/matrixfunction?param=" + param;
  let result = '';
  request.post(url, (error, response, body) => {
    result = JSON.parse(body);
    console.log(result);
  });

  return context
    .status(200)
    .succeed({'environment_variable': gateway_endpoint, 'param': param, 'response': result})
}

