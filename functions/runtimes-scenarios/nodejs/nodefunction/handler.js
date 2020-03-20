'use strict'

module.exports = async (event, context) => {
  const result = {
    'status': 'Hello From NodeJS Serverless Function'
  }

  return context
    .status(200)
    .succeed(result)
}

