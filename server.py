from flask import Flask, request, redirect
from flask_restful import Api, Resource
from colorama import init, Fore, Style
import sqlite3
import json
import os

DATA = os.path.join( os.path.dirname(__file__) , 'DATA' )
INBOX = os.path.join( DATA , 'INBOX' )
USERNAMES = os.path.join( DATA , 'usernames.db' )
MSG_COUNT = os.path.join( DATA , 'messagecount.txt' )
HOME_LIST = {
    'status': 'online',
    'github': 'https://github.com/msr8/snapmail'
}


if not os.path.exists(DATA):
    os.makedirs(DATA)
if not os.path.exists(INBOX):
    os.makedirs(INBOX)

def init_database():
    try:
        db_connection = sqlite3.connect(USERNAMES)
        crsr = db_connection.cursor()
        cmd = 'CREATE TABLE usernames ( username VARCHAR(20) PRIMARY KEY, password VARCHAR(20) )'
        crsr.execute(cmd)
        db_connection.close()
    except sqlite3.OperationalError:       pass
    if not os.path.exists(MSG_COUNT):
        with open(MSG_COUNT, 'w') as f:    pass

def get_msg_count():
    with open(MSG_COUNT) as f:
        ret = len(f.readlines())
    return ret

def check_pass(username, password):
    conn = sqlite3.connect(USERNAMES)
    crsr = conn.cursor()
    cmd = f'SELECT * FROM usernames WHERE username=="{username}" and password=="{password}"'
    crsr.execute(cmd)
    data = crsr.fetchall()
    conn.close()
    # Checks if the data is of any length
    if not len(data):
        return False
    # Checks if username and password is correct (to counter exploits)
    ret = True if data[0][1] == password else False
    return ret

cls = lambda: os.system('cls' if os.name == 'nt' else 'clear')



init_database()









app = Flask(__name__)
api = Api(app)



@app.route('/')
def test():
    return redirect('https://github.com/msr8/snapmail')


class Exists(Resource):
    def get(self, username):
        # Checks if the username exists
        db_connection = sqlite3.connect(USERNAMES)
        crsr = db_connection.cursor()
        crsr.execute(f'SELECT * FROM usernames WHERE username=="{username}"')
        ans = True if len(crsr.fetchall()) else False
        db_connection.close()
        # Returns the data
        return {'username':username , 'exists':ans}


class Signup(Resource):
    def post(self):
        try:
            # Gets the data given to us
            data = request.form
            username = data['username']
            password = data['password']
            # Executes the command in SQL
            conn = sqlite3.connect(USERNAMES)
            crsr = conn.cursor()
            cmd = f'INSERT INTO usernames VALUES ("{username}" , "{password}")'
            crsr.execute(cmd)
            conn.commit()
            conn.close()
            # Tells that it was a success
            return {'username':username , 'password':password , 'status':'success'}
        # In case of exception, tells what exception
        except Exception as e:
            return {'error':str(e)}


class Login(Resource):
    def post(self):
        try:
            # Gets the data given to us
            data = request.form
            username = data['username']
            password = data['password']
            matching = check_pass(username, password)
            return {'username':username , 'password':password , 'matching':matching}
        # In case of exception, tells what exception
        except Exception as e:
            return {'error':str(e)}


class Message(Resource):
    def post(self):
        try:
            # Gets the data given to us
            data = request.form
            username = data['username']
            password = data['password']
            # Checks if username and pass are correct
            if not check_pass(username, password):
                return {'error': 'Stop trying to spoof messages -_-'}
            destination = data['destination'].lower()
            # Check if they're teying to send msges to themself
            if destination == username:
                return {'error': 'You cannot send messages to yourself!'}
            mail_head = data['header'] if len(data['header']) <= 30 else '-'
            mail_body = data['body']

            # Gets the message id
            msg_id = str(get_msg_count() + 1)

            # Checks if the reciever json exists and gets the data
            recv_json = os.path.join(INBOX,f'{destination}.json')
            if os.path.isfile(recv_json):
                with open(recv_json) as rf:
                    prev_msges = json.load(rf)
            else:
                prev_msges = {}

            # Adds the message
            prev_msges[msg_id] = {'origin':username , 'header':mail_head , 'body':mail_body}
            # Saves it
            with open(recv_json, 'w') as wf:
                json.dump(prev_msges, wf, indent=2)
            # Adds 1 to the msg id
            with open(MSG_COUNT, 'a') as f:
                f.write('-\n')

            return {'status':'success'}

        except Exception as e:
            return {'error': str(e)}


class Inbox(Resource):
    def post(self):
        try:
            # Gets the data given to us
            data = request.form
            username = data['username']
            password = data['password']
            if not check_pass(username, password):
                return {'error': 'Stop trying to snoop messages -_-'}

            # Gets the messages
            json_file = os.path.join(INBOX,f'{username}.json')
            # If file not exists, sends an empty dict
            if not os.path.isfile(json_file):
                return {}
            with open(json_file) as f:
                msges = json.load(f)

            # Deletes the bodies
            for key in msges.keys():
                del msges[key]['body']

            # Returns the dict with bodies deletes
            return msges

        except Exception as e:
            return {'error': str(e)}


class Read(Resource):
    def post(self):
        try:
            # Gets the data given to us
            data = request.form
            username = data['username']
            password = data['password']
            msg_id = data['message_id']

            if not check_pass(username, password):
                return {'error': 'Stop trying to snoop messages -_-'}

            # Gets the messages
            json_file = os.path.join(INBOX,f'{username}.json')
            with open(json_file) as rf:
                msges = json.load(rf)

            # Checks if message is in the inbox
            if not msg_id in msges.keys():
                return {'error': 'The message you are trying to access is not present'}

            # Gets the message and deletes it from the json file
            msg_dic = msges[msg_id]
            del msges[msg_id]
            with open(json_file,'w') as wf:
                json.dump(msges, wf, indent=2)

            # Returns the message
            return msg_dic

        except Exception as e:
            return {'error': str(e)}








# Adds the links and make it accesible
api.add_resource(Exists, '/exists/<string:username>/')
api.add_resource(Signup, '/signup/')
api.add_resource(Login, '/login/')
api.add_resource(Message, '/message/')
api.add_resource(Inbox, '/inbox/')
api.add_resource(Read, '/read/')



if __name__ == '__main__':
    cls()
    print(f'{BOL}{GR}[TURNING ON SERVER]{RES}\n')

    from waitress import serve
    serve(app, port=5000, host='0.0.0.0')

    # app.run(debug=False)


