'use strict';
const request = require('request');


function doRequest(headers, url, data) {
  return new Promise(function (resolve, reject) {
    request.post({
      headers: headers,
      url:     url,
      body:    data
    }, function (error, res, body) {
      if (!error && res.statusCode == 200) {
          console.log(body);
          console.log(res);
        resolve(body);
      } else {
         console.log(error);
        reject(error);
      }
    });
  });
}

async function testEntry(url) {
  let res = await doRequest({"content-type": "text/plain"}, url, " ");
  console.log(res);
  console.log(res);
  console.log('This is Mohammed');
  return res
}

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
  let res =  await testEntry(url);
  if (res) {
          return context
            .status(200)
            .succeed(res)
  } else {
      return context.fail({"result": "Error while trying to call function"});
  }
};


