"""File handling module"""

import json, os
import logging
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


def load_data_from_json(path_file, encoding="utf-8"):
    try:
        with open(path_file, encoding=encoding) as json_file:
            data = json.load(json_file)
            return data
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logging.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ops... internal error! " + error_msg,
        )


def save_list_to_json(list_data, filename):
    try:
        # Check if the file exists, if not create it
        if not os.path.exists(filename):
            create_folder = os.path.dirname(filename)
            if not os.path.exists(create_folder):
                os.makedirs(create_folder)

            with open(filename, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

        # Save the list data to the JSON file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(list_data, f, ensure_ascii=False, indent=4)
            return True
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logging.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ops... internal error! " + error_msg,
        )
