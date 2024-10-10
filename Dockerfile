FROM python:3.11.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
# todo: Fix problem with using current requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# todo: Fix problem with werkzeug version 
COPY . .

CMD ["python", "app.py"]
