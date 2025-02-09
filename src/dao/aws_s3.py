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
