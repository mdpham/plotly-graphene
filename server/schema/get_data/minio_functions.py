#!/bin/python

import os

from minio import Minio
from minio import ResponseError

def get_client():
    return Minio(
        'minio:'+os.getenv('MINIO_HOST_PORT'),
        access_key=os.getenv('MINIO_ACCESS_KEY'),
        secret_key=os.getenv('MINIO_SECRET_KEY'),
        secure=False
    )

def object_exists(bucket, objct, minio_client):
    if (minio_client.bucket_exists(bucket)):
        for obj in minio_client.list_objects(bucket):
            if (obj.object_name == objct):
                return True
    return False

def format_line_as_string_list(line):
    return (
        str(line) # Convert to string
        [2:-1] # Remove b'' from b'<Stuff we need>'
        .rstrip("\\n") # '\' is interpreted literally for some reason
        .split("\\t")
    )

def get_first_line(bucket, objct, minio_client):
    return format_line_as_string_list(
        minio_client.get_object(bucket, objct).readline()
    )

def get_obj_as_2dlist(bucket, objct, minio_client, include_header=True):
    obj = minio_client.get_object(bucket, objct)
    if (not include_header):
        obj.readline()
    return [format_line_as_string_list(line) for line in obj]

