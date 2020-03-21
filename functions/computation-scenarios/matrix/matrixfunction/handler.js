'use strict'

const Matrix = require("./matrix.js");

module.exports = (event, context) => {
  console.log(event);
  console.log(context);
  let param = 1;
  const isExist = 'param' in event['query'];
  if (isExist) {
      param = event['query']['param']

  }
  console.log('Input param=' + param);
  const a = Matrix.create(param, param);
  const b = Matrix.create(param, param);
  const resultBig = Matrix.multiply(a, b);
  const result = {
    'result': Matrix.subset(resultBig, 0, 0, 10, 10)
  };

  return context
    .status(200)
    .succeed(result)
}

