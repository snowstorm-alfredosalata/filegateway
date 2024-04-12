#!/bin/bash

write_request=$(cat <<EOF
{
    "fs": {
        "fs": "osfs"
    },
    "content": "Ciao!",
    "path": "saluti.txt"
}
EOF
)

curl -X JSON -H "Content-Type: application/json" -d "$write_request" http://127.0.0.1:5000/api/v1/write_document

get_request=$(cat <<EOF
{
    "fs": {
        "fs": "osfs"
    },
    "path": "saluti.txt"
}
EOF
)

curl -X JSON -H "Content-Type: application/json" -d "$get_request" http://127.0.0.1:5000/api/v1/read_document