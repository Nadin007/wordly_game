FROM python:3.9
WORKDIR /code
COPY ./wordly_game_backednd/requirements.txt /code/wordly_game_backednd/requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /code/wordly_game_backednd/requirements.txt --no-cache-dir

COPY ./wordly_game_backednd /code
WORKDIR /code

CMD gunicorn wordly_game_backednd.wsgi:application --bind 0.0.0.0:8000