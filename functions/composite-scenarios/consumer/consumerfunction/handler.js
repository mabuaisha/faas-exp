'use strict'

module.exports = (event, context) => {
  const gateway = process.env.gateway_endpoint

  return context
    .status(200)
    .succeed({'environment_variable': gateway})
}

