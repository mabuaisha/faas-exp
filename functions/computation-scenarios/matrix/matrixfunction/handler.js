'use strict'

const Matrix = require("./matrix.js");

module.exports = async(event, context) => {
  console.log(event);
  console.log(context);
  let param = 1;
  const isExist = 'param' in event['query'];
  if (isExist) {
      param = event['query']['param']

  }
  console.log('Input param=' + param);
  const a = await Matrix.create(param, param);
  const b = await Matrix.create(param, param);
  const resultBig = await Matrix.multiply(a, b);
  const result = {
    'result': await Matrix.subset(resultBig, 0, 0, 10, 10)
  };

  return context
    .status(200)
    .succeed(result)
}

