import json
import logging
import time
from datetime import date, datetime, timedelta

import pandas as pd
import requests as rq
from fastapi import requests
from newsapi import NewsApiClient
from requests import ConnectionError, RequestException

import dynaconfig

# News API params loaded from settings.toml
API_KEY = dynaconfig.settings["NEWS_API"]["API_KEY"]
QUERY = dynaconfig.settings["NEWS_API"]["QUERY"]
LANGUAGE = dynaconfig.settings["NEWS_API"]["LANGUAGE"]
TIME_TO_PURGE = dynaconfig.settings["TIMINIGS"]["TIME_TO_PURGE"]
TIME_TO_SEARCH = dynaconfig.settings["TIMINIGS"]["TIME_TO_SEARCH"]
NEWS_DB_API_URL = dynaconfig.settings["DB"]["NEWS_DB_API_URL"]

newsapi = NewsApiClient(api_key=API_KEY)


# Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.WARNING
)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.ERROR
)


def is_api_available() -> bool:
    """
    Check is API available
    :return: bool
    """
    try:
        response = rq.get(f"{NEWS_DB_API_URL}/healthcheck")
        return response.ok
    except RequestException as req_exc:
        logging.error(req_exc)
        return False
    except requests.HTTPConnection as http_con:
        logging.error(http_con)
        return False


def fetch_info() -> dict:
    """
    Fetch info from API according to query in settings.toml
    This is the Extraction step in ETL pipeline
    :return: dictionary of data founded
    """
    # Use to get news from yesterday to current time
    yesterday = date.today() - timedelta(days=1)
    try:
        logging.info(
            f"Searching for {QUERY}; most popular; from: {yesterday}; language: {LANGUAGE}"
        )
        result = newsapi.get_everything(
            q=QUERY, sort_by="popularity", from_param=yesterday, language=LANGUAGE
        )
        return result
    except ConnectionError as con_err:
        logging.error(con_err)
        return {}
    except BaseException as base_err:
        logging.error(base_err)
        return {}


def send_to_db(fetch_info: dict):
    """
    Generator using to load specific info to db
    These are the Transform and Load steps in ETL pipeline
    :param fetch_info:
    :return:
    """
    if fetch_info:
        logging.info(f"Found about {fetch_info['totalResults']} entities.")
        articles_df = pd.DataFrame(fetch_info["articles"])
        del articles_df["source"]
        del articles_df["content"]
        del articles_df["urlToImage"]
        for article in articles_df.values:
            yield article
    else:
        logging.warning("Empty response from News API.")
        raise IndexError


if __name__ == "__main__":
    while True:
        CURRENT_TIME = datetime.now().strftime("%H:%M")
        time.sleep(1)
        if is_api_available():
            logging.info("Connected to API.")
            if CURRENT_TIME == TIME_TO_PURGE:
                logging.info(f"Time to purge has come !")
                try:
                    response = rq.get(f"{NEWS_DB_API_URL}/purge")
                except BaseException as base_err:
                    logging.error(f"BaseException: {base_err}")
            else:
                logging.info(f"Still waiting for purging.")

            if CURRENT_TIME == TIME_TO_SEARCH:
                logging.info("Time to search has come !")
                try:
                    for data_chunk in send_to_db(fetch_info()):
                        response = rq.post(
                            f"{NEWS_DB_API_URL}/insert",
                            data=json.dumps(list(data_chunk)),
                        )
                except ValueError as val_err:
                    logging.error(f"ValueError: {val_err}")
                except IndexError as ind_err:
                    logging.error(f"IndexError: {ind_err}")
                except BaseException as base_err:
                    logging.error(f"BaseException: {base_err}")
            else:
                logging.info("Still waiting for searching.")
        else:
            logging.error("API is not available !")
