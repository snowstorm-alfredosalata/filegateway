let write_request = {
    fs: {
        fs: "osfs",
    },
    path: "saluti.txt",
    content: "Ciao!"
}

await fetch("http://127.0.0.1:5000/write", {
  "headers": { "Content-type": "application/json"  },
  "body": JSON.stringify(write_request),
  "method": "POST"
}).then(async (a) => {
    console.log(await a.json())        
});

let get_request = {
    fs: {
        fs: "osfs",
    },
    path: "saluti.txt"
}

await fetch("http://127.0.0.1:5000/read", {
  "headers": { "Content-type": "application/json"  },
  "body": JSON.stringify(get_request),
  "method": "POST"
}).then(async (a) => {
    console.log(await a.text())
});
