from dotenv import load_dotenv, find_dotenv
import logging, os
import boto3
from botocore.exceptions import NoCredentialsError

# Environment variables
load_dotenv(find_dotenv())

env_keys = {
    "AWS_ID": os.environ.get("LIA_AWS_ID"),
    "AWS_KEY": os.environ.get("LIA_AWS_KEY"),
    "AWS_SELECTED_REGION": os.environ.get("AWS_SELECTED_REGION"),
}


def upload_to_aws_S3(local_file, bucket, s3_file):

    s3 = boto3.client(
        "s3",
        aws_access_key_id=env_keys.get("AWS_ID"),
        aws_secret_access_key=env_keys.get("AWS_KEY"),
    )

    try:
        s3.upload_file(local_file, bucket, s3_file)
        logging.info("Upload " + str(local_file) + " to S3 successfully!")
        return True
    except FileNotFoundError:
        logging.error("The file was not found")
        return False
    except NoCredentialsError:
        logging.error("Credentials not available")
        return False


def download_all_from_s3(bucket, s3_path, local_dir="/tmp"):

    s3 = boto3.client(
        "s3",
        aws_access_key_id=env_keys.get("AWS_ID"),
        aws_secret_access_key=env_keys.get("AWS_KEY"),
        region_name=env_keys.get("AWS_SELECTED_REGION"),
    )

    try:
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)

        paginator = s3.get_paginator("list_objects_v2")
        pages = paginator.paginate(Bucket=bucket, Prefix=s3_path)

        for page in pages:
            if "Contents" in page:
                for obj in page["Contents"]:
                    s3_file_path = obj["Key"]
                    local_file_path = os.path.join(
                        local_dir, os.path.basename(s3_file_path)
                    )
                    s3.download_file(bucket, s3_file_path, local_file_path)
                    logging.info(f"Downloaded {s3_file_path} to {local_file_path}")

        return True
    except NoCredentialsError:
        logging.error("Credentials not available")
        return False
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return False
