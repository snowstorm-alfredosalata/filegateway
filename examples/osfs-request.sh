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

curl -X POST -H "Content-Type: application/json" -d "$write_request" http://127.0.0.1:5000/write

get_request=$(cat <<EOF
{
    "fs": {
        "fs": "osfs"
    },
    "path": "saluti.txt"
}
EOF
)

curl -X POST -H "Content-Type: application/json" -d "$get_request" http://127.0.0.1:5000/read