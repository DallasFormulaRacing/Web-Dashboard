FROM python:3.7.1

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
# todo: Fix problem with using current requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# todo: Fix problem with werkzeug version 
RUN pip uninstall --yes werkzeug
RUN pip install -v https://github.com/pallets/werkzeug/archive/refs/tags/2.0.3.tar.gz
COPY ./app.py /code

CMD ["python", "app.py"]