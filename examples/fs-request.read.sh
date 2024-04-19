get_request=$(cat <<EOF
{
    "fs": {
        "fs": "os"
    },
    "path": "/sample.file"
}
EOF
)

curl -X POST -H "Content-Type: application/json" -d "$get_request" http://127.0.0.1:5000/read