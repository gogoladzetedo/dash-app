FROM python:3.9.6

RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD data/. /app/data/
ADD interface_helpers/. /app/interface_helpers/
ADD app.py /app/
ADD README.md /app/

ENTRYPOINT [ "python" ]
CMD ["app.py"]