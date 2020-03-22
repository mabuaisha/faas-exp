'use strict'

module.exports = (event, context) => {
  let number = event['body'];
  number = number.replace(/\n/g, '');
  console.log(event);
  console.log(context);

    if (!number || !isNumeric(number)) {
        return context
            .status(400)
            .fail(createErrorResponse("Please pass a valid number 'number'."));
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