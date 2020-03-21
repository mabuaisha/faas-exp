'use strict'

const fs = require('fs');

module.exports = (event, context) => {
  console.log(event);
  console.log(context);
  let writer = fs.createWriteStream('/tmp/log.txt', {
    flags: 'a' // 'a' means appending (old data will be preserved)
  });

  writer.write(event['body']);
  let buffer = fs.readFileSync('/tmp/log.txt');
  console.log(buffer.toString());
  const result = buffer.toString();
  return context
    .status(200)
    .succeed(result)
}

