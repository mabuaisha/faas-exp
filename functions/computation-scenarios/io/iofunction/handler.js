'use strict'

const fs = require('fs');

module.exports = async (event, context) => {
  console.log(event);
  console.log(context);
  let writer = fs.createWriteStream('/tmp/log.txt', {
    flags: 'a' // 'a' means appending (old data will be preserved)
  });

  writer.write(event['body']);
  return context
    .status(200)
    .succeed({'result': 'Write done'})
}

