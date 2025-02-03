from dotenv import load_dotenv, find_dotenv
import logging, os
import requests

# Environment variables
load_dotenv(find_dotenv())

env_keys = {
    "TELEGRAM_BOT_TOKEN": os.environ.get("TELEGRAM_BOT_TOKEN"),
    "TELEGRAM_MAIN_CHAT_ID": os.environ.get("TELEGRAM_MAIN_CHAT_ID"),
}


class LiaTelegram:
    def __init__(self):

        self.bot_token = env_keys.get("TELEGRAM_BOT_TOKEN")
        self.bot_main_chat_id = env_keys.get("TELEGRAM_MAIN_CHAT_ID")

    def send_simple_msg_chat(self, message: str = ""):

        try:
            url = (
                "https://api.telegram.org/bot"
                + self.bot_token
                + "/sendMessage?chat_id="
                + self.bot_main_chat_id
                + "&text="
                + message
                + "&parse_mode=markdown"
            )
            response = requests.request("GET", url=url)

            return response.json()

        # Display an error message if something goes wrong.
        except Exception as e:
            logging.error(str(e))
            return None
