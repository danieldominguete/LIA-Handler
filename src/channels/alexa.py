"""
Alexa Interface
"""

import logging
from dateutil.parser import parse
from dao.file import load_data_from_json, save_list_to_json
from dao.aws_s3 import upload_to_aws_S3
import uuid, datetime, os
from dotenv import load_dotenv, find_dotenv

# Environment variables
load_dotenv(find_dotenv())
ENV = os.getenv("ENV")


class LiaAlexa:
    def __init__(self):

        if ENV == "local":
            self.config = load_data_from_json("src/config/lia_alexa_feeds.json")
        else:
            self.config = load_data_from_json("config/lia_alexa_feeds.json")

    def register_flash_briefing_feed(self, message: str = "", title: str = ""):

        try:
            feeds = []
            date_ref_dt = datetime.datetime.now()
            date_ref = date_ref_dt.strftime("%Y-%m-%d %H:%M:%S")

            dt_update = parse(str(date_ref))
            dt_update = dt_update.isoformat(timespec="seconds", sep="T")
            dt_update = dt_update + ".0Z"

            feed_item = {
                "uid": str(uuid.uuid4()),
                "updateDate": dt_update,
                "titleText": title,
                "mainText": message,
                "redirectionUrl": "https://www.cognas.ai/",
            }
            feeds.append(feed_item)

            # saving local json file
            full_path = self.config.get("alexa_feeds_file_path") + self.config.get(
                "alexa_feeds_filename"
            )
            save_list_to_json(list_data=feeds, filename=full_path)

            # update AWS bucket
            bucket_name = self.config.get("alexa_feeds_aws_bucket")
            bucket_full_path = "feeds/" + self.config.get("alexa_feeds_filename")

            uploaded = upload_to_aws_S3(
                local_file=full_path, bucket=bucket_name, s3_file=bucket_full_path
            )

            logging.info("Alexa feeds file updated:" + str(uploaded))

            return uploaded

        # Display an error message if something goes wrong.
        except Exception as e:
            logging.error(str(e))
            return None
