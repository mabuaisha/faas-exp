'use strict'
const ftp = require("basic-ftp");
const fs = require('fs');

module.exports = async (event, context) => {

  const ftpHost = process.env.ftp_host;
  const ftpUser = process.env.ftp_user;
  const ftpPassword = process.env.ftp_password;

  if (!ftpHost) {
      return context.status.fail('ftp Host is missing')
  }
  if (!ftpUser) {
      return context.status.fail('ftp User is missing')
  }
  if (!ftpPassword) {
      return context.status.fail('ftp Password is missing')
  }

  let result = {};
  let ftpResult = await ftpHandler(ftpHost, ftpUser, ftpPassword);
  let statusCode = 200;
  if (!ftpResult) {
      statusCode = 400;
      ftpResult = 'Error on downloading file from FTP'
      result['error'] = ftpResult
  } else{
      result['text'] = ftpResult;
  }

  return context
    .status(statusCode)
    .succeed({'result': result})

}


async function ftpHandler(host, user, password) {
    let result = null;
    const client = new ftp.Client();
    client.ftp.verbose = true;
    try {
        await client.access({
            host: host,
            user: user,
            password: password,
        });
         let writer = fs.createWriteStream('/tmp/test.txt', {
            flags: 'w' // 'a' means appending (old data will be preserved)
          });
        await client.downloadTo(writer, "test.txt");
        let buffer = fs.readFileSync('/tmp/test.txt');
        result = buffer.toString();
    }
    catch(err) {
        console.log(err)
    }
    client.close();
    return result;
}