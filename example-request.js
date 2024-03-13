let write_request = {
    fs: {
        fs: "s3",
    
        endpoint_url: "",
        access_key_id: "",
        secret_access_key: "",
        bucket_name: "",
        region_name: ""
        
    },
    path: "saluti.txt",
    content: "Ciao!"
}

fetch("http://127.0.0.1:5000/api/v1/read_document", {
  "headers": { "Content-type": "application/json"  },
  "body": JSON.stringify(write_request),
  "method": "JSON"
}).then(async (a) => { 
    console.log(a)
    console.log(await a.json())        
});

let get_request = {
    fs: {
        fs: "s3",
    
        endpoint_url: "",
        access_key_id: "",
        secret_access_key: "",
        bucket_name: "",
        region_name: ""
        
    },
    path: "saluti.txt"
}

fetch("http://127.0.0.1:5000/api/v1/read_document", {
  "headers": { "Content-type": "application/json"  },
  "body": JSON.stringify(get_request),
  "method": "JSON"
}).then(async (a) => { 
    console.log(a)
    console.log(await a.text())        
});