#!/bin/sh

echo "connecting minio client to server"
mc alias set minio ${MINIO_URL} ${MINIO_ACCESS_KEY} ${MINIO_SECRET_KEY}

echo "creating bucket"
mc mb minio/bvsar

echo "setting bucket to public"
mc policy set download minio/bvsar
