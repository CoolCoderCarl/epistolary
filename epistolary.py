import json
import logging
import time
from datetime import date, datetime, timedelta
from typing import Dict, List

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
TIME_TO_SEARCH = dynaconfig.settings["TIMINIGS"]["TIME_TO_SEARCH"]
NEWS_DB_API_URL = dynaconfig.settings["DB"]["DB_API_URL"]


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


class Epistolary:

    # How long sleep in case of errors
    __err_pause = 5

    def is_api_available(self) -> bool:
        """
        Check is API available
        :return: bool
        """
        try:
            response = rq.get(f"{NEWS_DB_API_URL}/healthcheck")
            logging.info(f"API is available. URL: {NEWS_DB_API_URL}")
            return response.ok
        except RequestException as req_exc:
            logging.error(f"API is not available ! URL: {NEWS_DB_API_URL}")
            logging.error(req_exc)
            time.sleep(self.__err_pause)
            return False
        except requests.HTTPConnection as http_con:
            logging.error(f"API is not available ! URL: {NEWS_DB_API_URL}")
            logging.error(http_con)
            time.sleep(self.__err_pause)
            return False

    def extract_data(self) -> Dict:
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
            logging.info(f"Found about {result['totalResults']} entities.")
            return result
        except ConnectionError as con_err:
            logging.error(con_err)
            time.sleep(self.__err_pause)
            return {}
        except BaseException as base_err:
            logging.error(base_err)
            time.sleep(self.__err_pause)
            return {}

    def transform_data(self, extracted_data_from_api: Dict) -> List:
        """
        Generator using to load specific info to db
        These is the Transform step in ETL pipeline
        :param fetch_info:
        :return:
        """
        if extracted_data_from_api:
            articles_df = pd.DataFrame(extracted_data_from_api["articles"])
            del articles_df["source"]
            del articles_df["content"]
            del articles_df["urlToImage"]
            for article in articles_df.values:
                yield article
        else:
            logging.warning("Empty response from News API.")
            raise IndexError

    def load_data(self, transformed_data_from_api: List):
        """
        Send info into db via API
        These is the Load step in ETL pipeline
        :param transformed_data_from_api:
        :return:
        """
        try:
            response = rq.post(
                f"{NEWS_DB_API_URL}/insert",
                data=json.dumps(list(transformed_data_from_api)),
            )
            logging.info(f"Data successfully posted | {response.status_code}")
        except ValueError as val_err:
            logging.error(f"ValueError: {val_err}")
            time.sleep(self.__err_pause)
        except IndexError as ind_err:
            logging.error(f"IndexError: {ind_err}")
            time.sleep(self.__err_pause)
        except BaseException as base_err:
            logging.error(f"BaseException: {base_err}")
            time.sleep(self.__err_pause)


if __name__ == "__main__":
    newsapi = NewsApiClient(api_key=API_KEY)
    epistolary = Epistolary()
    while True:
        CURRENT_TIME = datetime.now().strftime("%H:%M")
        if epistolary.is_api_available():
            if CURRENT_TIME == TIME_TO_SEARCH:
                logging.info("Time to search has come !")
                for transformed_data_from_api in epistolary.transform_data(
                    epistolary.extract_data()
                ):
                    epistolary.load_data(transformed_data_from_api)
                else:
                    logging.info("All data sent ! Take a break.")
                    time.sleep(60)
            else:
                logging.info("Still waiting for searching.")
                time.sleep(5)
