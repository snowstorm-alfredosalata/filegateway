#!/bin/bash

file_content=$(base64 ./sample.file)
write_request=$(cat <<EOF
{
    "fs": {
        "fs": "os"
    },
    "path": "/sample.file",
    "content": "$file_content"
}
EOF
)

curl -X POST -H "Content-Type: application/json" -d "$write_request" http://127.0.0.1:5000/write
