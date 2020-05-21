'use strict';

module.exports = async (event, context) => {
  const result = {'result': 'Received input: ' + JSON.stringify(event.body)};

  return context
    .status(200)
    .succeed(result)
};

