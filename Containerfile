FROM h0d0user/emperor_pandas:latest as builder

WORKDIR /opt

COPY ["epistolary.py", "/opt/"]
COPY ["dynaconfig.py", "/opt/"]
COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

FROM builder

CMD ["python3.9", "epistolary.py"]