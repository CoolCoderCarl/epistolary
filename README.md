# epistolary
Simple ETL getting info from https://newsapi.org/ and send to API 

## Prehistory
This simple service help to search information automatically via News API

> Epistolary examines the reports and prepares them for recording  
> (c) Author

## How to use
Need to fill `settings.toml` with next important variables:
1) `API_KEY`. You can find this data here - https://my.telegram.org/apps
2) `QUERY`. Key word to search for in articles.
3) `API_TOKEN`. Ask *BotFather* in telegram.
4) `CHAT_ID`. Use this to find chat ID where you want to send messages - https://api.telegram.org/botAPI_TOKEN/getUpdates
5) Check the main repo - https://github.com/CoolCoderCarl/datapath - get `docker-compose.yaml`
6) `docker-compose up -d`
7) ...
8) PROFIT !!!


```
[DB]
DB_API_URL = "http://attainments_sanctuary:8888"

[NEWS_API]
API_KEY = ""
QUERY = "computer science"
LANGUAGE = "en"

[TELEGRAM]
API_TOKEN = ""
CHAT_ID = ""

[TIMINIGS]
TIME_TO_PURGE = "00:00"
TIME_TO_SEARCH = "02:00"
TIME_TO_SEND_START = "10:00"
TIME_TO_SEND_END = "20:00"
SENDING_INTERVAL = 300
```

**Still have questions ? Google it.**