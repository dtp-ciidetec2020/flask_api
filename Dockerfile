FROM python:3.6

COPY . /flask_api
WORKDIR  /flask_api	
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver"]


