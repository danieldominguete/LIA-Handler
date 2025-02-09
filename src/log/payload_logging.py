"""Payload logging module"""

import logging, os
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from schemas.data_request import ExampleResponseBody
from dao.file import save_dict_to_json
from dao.aws_s3 import upload_to_aws_S3
from dotenv import load_dotenv, find_dotenv

# Environment variables
load_dotenv(find_dotenv())
ENV = os.getenv("ENV")

PATH_LOCALHOST = "tmp/log" + "/" + ENV
PATH_S3 = "log" + "/" + ENV
BUCKET = "lia-handler"


def save_response_to_s3(response: ExampleResponseBody) -> bool:

    try:
        # save the response to json file
        filename_localhost = (
            PATH_LOCALHOST
            + "/"
            + str(response.get("service"))
            + "/date="
            + str(response.get("datetime"))
            + "/"
            + str(response.get("id"))
            + ".json"
        )
        save_dict_to_json(response, filename_localhost)

        # Save the response to S3
        filename_s3 = (
            PATH_S3
            + "/"
            + str(response.get("service"))
            + "/date="
            + str(response.get("datetime"))
            + "/"
            + str(response.get("id"))
            + ".json"
        )
        uploaded = upload_to_aws_S3(
            local_file=filename_localhost,
            bucket=BUCKET,
            s3_file="lia_logs/" + filename_s3,
        )
        return uploaded
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logging.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ops... internal error! " + error_msg,
        )
