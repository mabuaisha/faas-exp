'use strict'

module.exports = (event, context) => {
  let number = event['body'];

    if (!number || !isNumeric(number)) {
        return context
            .status(400)
            .failed(createErrorResponse("Please pass a valid number 'number'."));
    }

    number = parseInt(number);
    const result = fib(number);

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