FROM python

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir    

COPY *.py ./

CMD [ "python", "main.py" ]