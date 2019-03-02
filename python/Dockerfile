FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PBR_VERSION 1.0

RUN python setup.py install

EXPOSE 8080

CMD [ "python", "./src/main/restbyexample/phonebook/pecan/run_cheroot.py" ]

