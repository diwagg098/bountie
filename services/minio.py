import io
from datetime import datetime
from os import getenv
from fastapi import UploadFile
from minio import Minio


def get_minio_client():
    client = Minio(
        getenv("MINIO_URL"),
        access_key=getenv("MINIO_ACCESS_KEY"),
        secret_key=getenv("MINIO_SECRET_KEY"),
        secure=False
    )
    return client


async def upload_image_file(bucket_name: str, file: UploadFile, image_name: str = None):
    minio_client = get_minio_client()
    # The File type is SpooledTemporary File
    # Read and Convert into bytes IO
    image_file = await file.read()
    image_size = len(image_file)
    image_byte = io.BytesIO(image_file)
    if image_name is None:
        image_name = f"{file.filename}_{datetime.now()}"

    found = minio_client.bucket_exists(bucket_name)
    if not found:
        minio_client.make_bucket(bucket_name)

    minio_client.put_object(
        bucket_name=bucket_name,
        object_name=image_name,
        length=image_size,
        data=image_byte,
        content_type=file.content_type)

    await file.close()

    image_url = f"{getenv('MINIO_PUBLIC_URL')}{bucket_name}/{image_name}"

    return {
        "image_url": image_url
    }
