import os

import psycopg2
from psycopg2 import Error


def biult_stat(request_user_id):
    try:
        connection = psycopg2.connect(
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            host=os.environ.get('DB_HOST'),
            port='5432',
            database=os.environ.get('DB_NAME')
        )
        cursor = connection.cursor()
        game_played = (
            "SELECT sec.id, COUNT(*) AS Played "
            "FROM wordly_features_daychallenge As fr INNER JOIN user_user AS sec ON fr.player_id = sec.id "
            "Where fr.is_active = 'False' AND sec.id = %s"
            "Group By sec.id")
        amount_won = (
            "With get_arr1 (word, attempt, player, task) AS ("
            "Select word, attempt, chal.player_id AS player, chal.word_id As task "
            "From wordly_features_userword As game Inner Join wordly_features_words AS wr_bank ON game.word_id = wr_bank.id "
            "Inner Join wordly_features_daychallenge As chal On game.task_id = chal.id "
            "Where chal.player_id = %s), "
            "get_task_word (task, mean_tsk) "
            "AS (Select chal.word_id, word "
            "From wordly_features_words AS wr_bank Inner Join wordly_features_daychallenge AS chal ON chal.word_id = wr_bank.id) "
            "Select player, attempt, word, mean_tsk "
            "From get_arr1 Inner Join get_task_word Using(task) "
            "Where mean_tsk = word "
        )
        cursor.execute(game_played, [request_user_id])
        result_1 = cursor.fetchall()

        cursor.execute(amount_won, [request_user_id])
        result_2 = cursor.fetchall()

        if result_1[0][0] == result_2[0][0]:
            stat = {'user_id': result_2[0][0], 'attempt': result_1[0][1], 'solved': [0, 0, 0, 0, 0, 0]}
            for vct in result_2:
                if vct[1] == 1:
                    stat.get('solved')[0] += 1
                elif vct[1] == 2:
                    stat.get('solved')[1] += 1
                elif vct[1] == 3:
                    stat.get('solved')[2] += 1
                elif vct[1] == 4:
                    stat.get('solved')[3] += 1
                elif vct[1] == 5:
                    stat.get('solved')[4] += 1
                elif vct[1] == 6:
                    stat.get('solved')[5] += 1

    except (Exception, Error) as error:
        print("An error occurred while working with PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Connection with PostgreSQL is closed")
        return stat
