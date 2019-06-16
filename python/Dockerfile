FROM python:3.7-alpine3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .tox/dist/phonebook_pecan-*.zip .
RUN pip install --no-cache-dir phonebook_pecan-*.zip

EXPOSE 8080

CMD [ "python", "/usr/local/lib/python3.7/site-packages/restbyexample/phonebook/pecan/run_cheroot.py" ]

