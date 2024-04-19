#!/bin/bash

read -p "Enter your AWS access key ID: " access_key_id
read -p "Enter your AWS secret access key: " secret_access_key
read -p "Enter your AWS bucket name: " bucket_name
read -p "Enter your AWS region name: " region_name

endpoint_url="https://s3-$region_name.amazonaws.com"

get_request=$(cat <<EOF
{
    "fs": {
        "fs": "s3",
        "endpoint_url": "$endpoint_url",
        "access_key_id": "$access_key_id",
        "secret_access_key": "$secret_access_key",
        "bucket_name": "$bucket_name",
        "region_name": "$region_name"
    },
    "path": "/sample.file"
}
EOF
)

curl -X POST -H "Content-Type: application/json" -d "$get_request" http://127.0.0.1:5000/read