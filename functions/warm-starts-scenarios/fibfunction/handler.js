'use strict'

module.exports = async (event, context) => {
  let number = event['query']['param'];
  console.log(event);
  console.log(context);
  number = number.replace(/\n/g, '');

    if (!number || !isNumeric(number)) {
        return context
            .status(400)
            .fail(createErrorResponse("Please pass a valid number 'number'."));
    }

    number = await parseInt(number);
    const result = await fib(number);

  return context
    .status(200)
    .succeed({'result': result})
};

let fib = function(n) {
    if (n <= 1) {
        return 1;
    } else {
        return fib(n - 1) + fib(n - 2);
    }
};

let createErrorResponse = function (message) {
    let response = {
        result: "[400] " + message,
    };

    return JSON.stringify(response);
};

let isNumeric = function(value) {
    return /^\d+$/.test(value);
};