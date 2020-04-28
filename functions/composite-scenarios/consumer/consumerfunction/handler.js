'use strict'
const request = require('sync-request');


let doRequest = function(url) {

  let result = null;
  let res = request('GET', url);
  let statusCode = res.statusCode;
  if (statusCode == 200) {
       result = JSON.parse(res.getBody('utf8'));
       console.log(result);
  } else {
      result = 'unable to call matrixfunction';
  }
  res['statusCode'] = statusCode;
  res['result'] = result;
  return res;
};

module.exports = async(event, context, callback) => {
  const gateway_endpoint = process.env.gateway_endpoint;

  if (!gateway_endpoint) {
      return context.status.fail('Gateway URL is missing')
  }
  let param = 1;
  const isExist = 'param' in event['query'];
  if (isExist) {
      param = event['query']['param']

  }
  // This call to a matrix function
  const url = gateway_endpoint + "/function/matrixfunction?param=" + param;
  let res = await doRequest(url);
  if (res['statusCode'] == 200) {
        return context.status(res['statusCode']).succeed(res['result']);
  } else {
      return context.fail(res['result']);
  }
}


