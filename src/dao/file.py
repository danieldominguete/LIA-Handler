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
            new_folder = os.path.dirname(filename)
            if not os.path.exists(new_folder):
                os.makedirs(new_folder, exist_ok=True)

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


def save_dict_to_json(dict_data, filename):
    try:
        # Check if the file exists, if not create it
        if not os.path.exists(filename):
            new_folder = os.path.dirname(filename)
            if not os.path.exists(new_folder):
                os.makedirs(new_folder, exist_ok=True)

        # Save the list data to the JSON file
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dict_data, f, ensure_ascii=False, indent=4)
            return True
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        logging.error(error_msg)
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ops... internal error! " + error_msg,
        )


def create_folder(folder_path: str) -> bool:
    """
    Create a new folder at the specified path if it doesn't already exist.

    This function attempts to create a new directory at the given path.
    If the directory already exists, the function will not create a new one.

    Args:
        folder_path (str): The path where the new folder should be created.

    Returns:
        bool: True if a new folder was created, None otherwise.

    Note:
        - This function uses os.path.exists() to check if the folder already exists.
        - It uses os.makedirs() to create the new directory.
        - If the folder already exists, the function will not raise an error,
          it will simply return None.
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
        return True
