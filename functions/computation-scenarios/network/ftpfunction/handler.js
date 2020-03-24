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

  console.log(event);
  console.log(context);
  console.log(ftpHost);
  console.log(ftpUser);
  console.log(ftpPassword);

  let ftpResult = await ftpHandler(ftpHost, ftpUser, ftpPassword);
  let statusCode = 400;
  let message = 'Error on downloading file';
  if (ftpResult) {
      statusCode = 22;
      message = 'Download succuessfully passed';
  }

  return context
    .status(statusCode)
    .succeed({'message': message})

}


async function ftpHandler(host, user, password) {
    let succeed = false;
    const client = new ftp.Client();
    client.ftp.verbose = true;
    try {
        await client.access({
            host: host,
            user: user,
            password: password,
        });
        console.log(await client.list());
         let writer = fs.createWriteStream('/tmp/log.txt', {
            flags: 'a' // 'a' means appending (old data will be preserved)
          });
        await client.downloadTo(writer, "test.txt");
        succeed = true;
    }
    catch(err) {
        console.log(err)
    }
    client.close();
    return succeed;
}