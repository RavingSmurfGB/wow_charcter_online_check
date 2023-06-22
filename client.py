import mysql.connector as mysql
import time, yaml, paramiko, logging
from yaml.loader import SafeLoader


logging.basicConfig(
    format="%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    filename='client.log',
    level=logging.INFO

)
logging.info("wow_character_online_check - started")

def get_config()-> dict:
    try:
        with open('config.env') as data:
            data = yaml.load(data, Loader=SafeLoader)
        return data
    except Exception as e:
        logging.critical("COULD NOT LOAD CONFIG.ENV - " , e)




def check_if_players_online(data:dict) -> bool:
    #returns true if character online

    try:
        host = data["MYSQL_HOST"]
        password = data["MYSQL_PASSWORD"]



        # connect to MySQL server
        
        db_connection = mysql.connect(host=host, database="tbccharacters",user="wow_character_check", password=password)


        # Get a cursor
        database_cursor = db_connection.cursor()


        # Select all from characters table
        database_cursor.execute("SELECT * FROM `characters`;")

        # Fetch one result
        returned_data = database_cursor.fetchall()

        character_online = None
        for character in returned_data:
            # If character is online (if variable 19 "onlin" in table characters = 1 )
            if character[19] == 1:
                character_online = True

        # Close connection
        database_cursor.close()

        #If there is a character online
        if character_online:
            return character_online
        
        else:
            return False
    except:
        logging.info("Could not connect via MYSQL - probably offline - retry in 1 minute")
        time.sleep(60)
    

def shutdown_server(data:dict):    

    host = data["SSH_HOST"]
    user = data["SSH_USER"]
    password = data["SSH_PASSWORD"]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=user, password=password)
    client.exec_command("/sbin/shutdown.sh && /sbin/poweroff")
    client.close()


def wait_10_mins_and_check_again():
    # If players are not online wait 10 minutes
    if not check_if_players_online(get_config()):
        logging.info("players not online - waiting 10 minutes for activity")
        time.sleep(600)

        #Then if no players are online after 10 minute wait:
        if not check_if_players_online(get_config()):
            logging.info("players are not online after 10 minute wait - shutting down")
            shutdown_server(get_config())

        #Then if players are online after 10 minute wait:
        elif check_if_players_online(get_config()):
            logging.info("players are online after 10 minute wait - staying online")
            return
        
    #If players are online
    elif check_if_players_online(get_config()):
        #wait 5 minutes and try again
        logging.info("players are online - waiting 5 minutes then recheck")
        time.sleep(300)
        return


if __name__ == '__main__':
    
    while True:
        wait_10_mins_and_check_again()





