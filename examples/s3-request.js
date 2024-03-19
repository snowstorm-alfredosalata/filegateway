const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const prompt = (query) => new Promise((resolve) => rl.question(query, resolve));

let access_key_id, secret_access_key, bucket_name, region_name;

(async() => {
  try {
    access_key_id = await prompt('Enter your AWS access key ID: ')
    secret_access_key = await prompt('Enter your AWS secret access key: ');
    bucket_name = await prompt('Enter your AWS bucket name: ',)
    region_name = await prompt('Enter your AWS region name: ',)
    
    rl.close();
  } catch (e) {
    console.error("Unable to prompt", e);
  }
})();

rl.on('close', async () =>  {

  const endpoint_url = `https://s3-${region_name}.amazonaws.com`

  let write_request = {
      fs: {
          fs: "s3",
      
          endpoint_url: endpoint_url,
          access_key_id: access_key_id,
          secret_access_key: secret_access_key,
          bucket_name: bucket_name,
          region_name: region_name
          
      },
      path: "saluti.txt",
      content: "Ciao!"
  }

  await fetch("http://127.0.0.1:8000/api/v1/write_document", {
    "headers": { "Content-type": "application/json"  },
    "body": JSON.stringify(write_request),
    "method": "JSON"
  }).then(async (a) => {
      console.log(await a.json())        
  });

  let get_request = {
      fs: {
          fs: "s3",
      
          endpoint_url: endpoint_url,
          access_key_id: access_key_id,
          secret_access_key: secret_access_key,
          bucket_name: bucket_name,
          region_name: region_name
          
      },
      path: "saluti.txt"
  }

  await fetch("http://127.0.0.1:8000/api/v1/read_document", {
    "headers": { "Content-type": "application/json"  },
    "body": JSON.stringify(get_request),
    "method": "JSON"
  }).then(async (a) => {
      console.log(await a.text())
  });

})
