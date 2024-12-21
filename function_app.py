import azure.functions as func
import logging
import psycopg2 as db
from psycopg2 import sql
import os
import datetime
from utils import create_table,generate_leaderboard_card


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name = 'newResult')
@app.route(route="newResult",methods=["post"])
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    body = req.get_json()
    msg = body['body']['body']['content']

    score = int(msg.split('/')[0][-6:].replace(',',''))
    version = int(msg[15:18])

    player = body['from']['user']['displayName']
    player_id = body['from']['user']['id']

    msg_timestamp = body['sent']


    
    
    cnx = db.connect(user=f"{os.getenv('db_user')}", password=f"{os.getenv('db_password')}", host=f"{os.getenv('db_host')}", port=f"{os.getenv('db_port')}", database=f"{os.getenv('db_name')}") 
   
    cur = cnx.cursor()

    cur.execute(f"INSERT INTO tg.results(playerid,playername,timeguessrversion,result,message_time,timestamp) VALUES ('{player_id}','{player}',{version},{score},'{msg_timestamp}','{datetime.datetime.now()}')")

    cnx.commit()

    cur.close()
    cnx.close()

    return_msg = f"Score = {score}, PLayer = {player},Version = {version}, player_id = {player_id}"

  
    return func.HttpResponse(
             return_msg,
             status_code=200
        )

@app.function_name(name='dailyLeaderboard')
@app.route(route="dailyLeaderboard",methods=["get"])
def dailyLeaderBoard(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    date = req.params.get("date")

    if date.isdigit():
        date = int(date)
    else:
        return func.HttpResponse(
            "The provided date must be on the format 'ddMMyyyy'",
            status_code=400
        )
    
    
    cnx = db.connect(user=f"{os.getenv('db_user')}", password=f"{os.getenv('db_password')}", host=f"{os.getenv('db_host')}", port=f"{os.getenv('db_port')}", database=f"{os.getenv('db_name')}") 
    cur = cnx.cursor()

    query = sql.SQL("SELECT ROW_NUMBER() OVER(ORDER BY MAX(r.result) desc),r.playername,MAX(r.result), d.date FROM tg.results r JOIN tg.dateversion d ON r.timeguessrversion = d.version WHERE d.date = %s GROUP BY r.playername, d.date ORDER BY MAX(result) DESC")
    cur.execute(query,(date,))
    result = cur.fetchall()

    cnx.commit()

    cur.close()
    cnx.close()
    return_msg = f'Leaderboard for date {date}'

    return_msg = generate_leaderboard_card(return_msg,result)

    return func.HttpResponse(
             return_msg,
             status_code=200
        )


@app.function_name(name='allTimeTop10')
@app.route(route="allTimeTop10",methods=["get"])
def dailyLeaderBoard(req: func.HttpRequest) -> func.HttpResponse:
    
    cnx = db.connect(user=f"{os.getenv('db_user')}", password=f"{os.getenv('db_password')}", host=f"{os.getenv('db_host')}", port=f"{os.getenv('db_port')}", database=f"{os.getenv('db_name')}") 
   
    cur = cnx.cursor()

    query = sql.SQL("SELECT ROW_NUMBER() OVER(ORDER BY r.result desc), r.playername,r.result, d.date FROM tg.results r JOIN tg.dateVersion d ON r.timeguessrVersion = d.version ORDER BY result DESC")
    cur.execute(query)
    result = cur.fetchmany(10)

    cnx.commit()

    cur.close()
    cnx.close()
    return_msg = f'All time top 10 scores'

    return_msg = generate_leaderboard_card(return_msg,result)

    return func.HttpResponse(
             return_msg,
             status_code=200
        )

