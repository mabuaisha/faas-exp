'use strict'

module.exports = (event, context) => {
  const gateway = process.env.gateway_endpoint

  console.log(event);
  console.log(context);
  let param = 1;
  const isExist = 'param' in event['query'];
  if (isExist) {
      param = event['query']['param']

  }

  return context
    .status(200)
    .succeed({'environment_variable': gateway, 'param': param})
}

