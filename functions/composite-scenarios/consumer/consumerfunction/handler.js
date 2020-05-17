'use strict';
const request = require('request');


let doRequest = async function(url) {

    let result = null;
    request(url, function (error, response, body) {
        let statusCode = response.statusCode;
        if (error) {
            console.error('upload failed:', error);
            result['statusCode'] = statusCode;
            result['result'] = error;
            return result
        } else {
            console.log(result);
            result['statusCode'] = statusCode;
            result['result'] = JSON.parse(response.body);
            return result
        }
    });

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
};


