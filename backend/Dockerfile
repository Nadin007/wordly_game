FROM python:3.9-slim

COPY ./wordly_game_backednd/requirements.txt /code/wordly_game_backednd/requirements.txt
RUN python3 -m pip install --upgrade pip && pip install -r /code/wordly_game_backednd/requirements.txt

COPY ./ /code
WORKDIR /code/wordly_game_backednd/

CMD gunicorn wordly_game_backednd.wsgi:application --bind 0.0.0.0:8000