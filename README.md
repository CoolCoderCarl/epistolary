# epistolary
Simple ETL getting info from https://newsapi.org/ and send to API.  
This service help to search information automatically via News API.  
First part of a system which search, save and share info.  

## Prehistory
Someone has to work and prepare the reports.

> Epistolary examines the reports and prepares them for recording  
> (c) Author

Enjoy.

## How to use
Need to fill `settings.toml` with next important variables:
1) `API_KEY`. You can find this data here - https://my.telegram.org/apps
2) `QUERY`. Key word to search for in articles.
3) `API_TOKEN`. Ask *BotFather* in telegram.
4) `CHAT_ID`. Use this to find chat ID where you want to send messages - https://api.telegram.org/botAPI_TOKEN/getUpdates
5) `docker-compose up -d` or `make dstart`
6) ...
7) PROFIT !!!


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
TIME_TO_SEARCH = "02:00"
TIME_TO_SEND_START = "10:00"
TIME_TO_SEND_END = "20:00"
SENDING_INTERVAL = 300
```

For more info check:
1) API & DB repo - https://github.com/CoolCoderCarl/attainments_sanctuary  
2) ETL repo - https://github.com/CoolCoderCarl/datapath

**Still have questions ? Google it.**