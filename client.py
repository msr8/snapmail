from colorama import init,Fore, Style
from prettytable import PrettyTable
from stuff import LOGO, HOME_LOGO
from getpass import getpass
import requests as rq
import platform as pf
import time as t
import argparse
import sys
import os
init()
# Gets the arguments given to us through the command line
parser = argparse.ArgumentParser(description='SNAPMAIL - An open source mail service which deletes your emails once you read them! Learn more at https://github.com/msr8/snapmail')
parser.add_argument('-t', '--tor', action='store_true', help='Reroutes all traffic through TOR')
args = parser.parse_args()



# Sees if we enabled TOR or not
TOR_ENABLED = args.tor
# Gets TOR proxies if TOR is enabled
PROXIES = {} if not TOR_ENABLED else {
    'http':  'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
    }

BASE_URL = rq.get(f'https://msr8.github.io/snapmail/{"clearnet" if not TOR_ENABLED else "darknet"}', proxies=PROXIES).text.strip()
SYSTEM = pf.system()

def slow_line_type(to_type):
    for line in to_type.split('\n'):
        print(line)
        t.sleep(0.2)

def get_wifi():
    profiles = []
    wifis = {}
    profiles_output = os.popen('netsh wlan show profiles').read()
    # Goes thro the lines
    for line in profiles_output.split('\n'):
        # Checks if its like 'All User Profile : Redmi'
        if not line.strip().startswith('All User Profile'):
            continue
        # Gets the profile name and adds it in our list
        profile = line.split(':')[1].strip()
        profiles.append(profile)
    # Goes thro all the profiles
    for profile in profiles:
        pw_output = os.popen(f'netsh wlan show profile "{profile}" key=clear').read()
        # Goes thro all the lines
        for line in pw_output.split('\n'):
            # Checks if it contains a password
            if not line.strip().startswith('Key Content'):
                continue
            password = line.split(':')[1].strip()
            wifis[profile] = password
    # Checks which wifis didnt have a password
    for profile in profiles:
        if not profile in wifis.keys():
            wifis[profile] = None
    return wifis

def get_network_information():
    CY = Fore.CYAN
    RES = Style.RESET_ALL
    print(f'{Style.BRIGHT}{Fore.YELLOW}[+] Gathering network data{RES}\n')
    ip = rq.get('https://api.ipify.org', proxies=PROXIES).text
    # Checks if we're on TOR
    if not TOR_ENABLED:
        data = rq.get(f'https://api.iplocation.net/?ip={ip}', proxies=PROXIES).json()
        ip_v = data['ip_version']
        country = data['country_name']
        isp = data['isp']
    # If TOR is enabled, gets relay data
    else:
        ip_v = isp = '?'
        data = rq.get(f'https://onionoo.torproject.org/details?limit=1&search={ip}', proxies=PROXIES).json()
        data = data['relays'][0]
        country = data['country_name']
        nickname = data['nickname']
        fingerprint = data['fingerprint']
    myTable = PrettyTable(  [f'{CY}Attribute{RES}',         f'{CY}Value{RES}'       ])
    myTable.add_row(        [f'{CY}IP{RES}',                f'{ip} (IPv{ip_v})'     ])
    myTable.add_row(        [f'{CY}Location{RES}',          country                 ])
    myTable.add_row(        [f'{CY}ISP{RES}',               isp                     ])
    # Adds the relay data if we're on TOR
    if TOR_ENABLED:
        myTable.add_row(    [f'{CY}Relay Nickname{RES}',    nickname                ])
        myTable.add_row(    [f'{CY}Relay Fingerprint{RES}', fingerprint             ])
    myTable.align[f'{CY}Attribute{RES}'] = 'l'
    myTable.align[f'{CY}Value{RES}'] = 'l'
    print(myTable)
    print(f'\n{Style.BRIGHT}{Fore.YELLOW}\n[+] Gathering WiFi passwords{RES}\n')
    
    if SYSTEM == 'Windows':
        wifis = get_wifi()
        lis = [ [key,wifis[key]] for key in wifis ]
        myTable = PrettyTable( [f'{CY}Name{RES}',f'{CY}Password{RES}'] )
        myTable.add_rows(lis)
        myTable.align[f'{CY}Attribute{RES}'] = 'l'
        myTable.align[f'{CY}Password{RES}'] = 'l'
        print(myTable)
    else:
        print('Not a windows distribution')

tor_text = lambda: f'{Style.BRIGHT}TOR:{Style.RESET_ALL} {f"{Fore.GREEN}Enabled" if TOR_ENABLED else f"{Fore.RED}Disabled"}{Style.RESET_ALL}  |  {BASE_URL.replace("https://","").replace("http://","").strip("/")}'

cls = lambda: os.system('cls' if SYSTEM=='Windows' else 'clear')
cls()    
















slow_line_type(f'{Fore.MAGENTA}{LOGO}{Fore.RESET}')
print(tor_text())
while True:
    print(f'{Style.BRIGHT}\nWelcome to Snapmail! What would you like to do?{Style.RESET_ALL}\n')
    print(f'{Fore.CYAN}[1]{Fore.RESET} {Fore.YELLOW}Login{Fore.RESET}')
    print(f'{Fore.CYAN}[2]{Fore.RESET} {Fore.YELLOW}Signup{Fore.RESET}')
    print(f'{Fore.CYAN}[3]{Fore.RESET} {Fore.YELLOW}Network Information {Style.BRIGHT}(FOR YOUR EYES ONLY!){Style.RESET_ALL}')
    print(f'{Fore.CYAN}[4]{Fore.RESET} {Fore.YELLOW}Exit{Fore.RESET}')
    signup_or_login = input('\n').lower()
    if not signup_or_login in ['1','2','3','4','login','signup','exit']:
        cls()
        print(f'{Fore.RED}{Style.BRIGHT}ERROR: Please select a valid option{Style.RESET_ALL}\n')
        continue
    if signup_or_login in ['3']:
        cls()
        get_network_information()
        input(f'\n\n\n{Style.BRIGHT}Press enter to continue{Style.RESET_ALL}\n')
        cls()
        print(f'{Fore.MAGENTA}{LOGO}{Fore.RESET}')
        print(tor_text())
        continue
    break

cls()

if signup_or_login in ['4','exit']:
    sys.exit()










# ---------------------------------------------------------------------------------------------------- SIGNUP ----------------------------------------------------------------------------------------------------

elif signup_or_login in ['2','signup']:
    # Loop until valid credentials are entered
    while True:
        print(f'{Style.BRIGHT}Username and password must be between 3-20 characters long and should contain only alpha-numeric characters. Username is NOT case sensitive{Style.RESET_ALL}\n')
        print(f'{Fore.RED}{Style.BRIGHT}NOTE: ONCE YOU SET YOUR USERNAME IT CANNOT BE CHANGED!!{Style.RESET_ALL}\n')
        username = input(f'{Style.BRIGHT}username:{Style.RESET_ALL} ').lower()
        password = getpass(f'{Style.BRIGHT}password:{Style.RESET_ALL} ')
        password_confirm = getpass(f'{Style.BRIGHT}Please reenter the password:{Style.RESET_ALL} ')

        cls()
        # Checks if the username is between 3 and 20 chars long
        if not (len(username) >= 3 and len(username) <= 20):
            print(f'{Fore.RED}{Style.BRIGHT}ERROR: Please make sure that the username is atleast 3 characters long and at maximum, 20 characters long{Style.RESET_ALL}\n')
            continue
        # Checks if the username is alphanumeric
        if not username.isalnum():
            print(f'{Fore.RED}{Style.BRIGHT}ERROR: Please make sure that the username only contains alphabets and numbers{Style.RESET_ALL}\n')
            continue
        # Checks if the password is between 3 and 20 chars long
        if not (len(password) >= 3 and len(password) <= 20):
            print(f'{Fore.RED}{Style.BRIGHT}ERROR: Please make sure that the password is atleast 3 characters long and at maximum, 20 characters long{Style.RESET_ALL}\n')
            continue
        # Checks if the password is alphanumeric
        if not password.isalnum():
            print(f'{Fore.RED}{Style.BRIGHT}ERROR: Please make sure that the password only contains alphabets and numbers{Style.RESET_ALL}\n')
            continue
        # Checks if password and confirmation password match
        if not password == password_confirm:
            print(f'{Fore.RED}{Style.BRIGHT}ERROR: Passwords do not match, please make sure you type the same password both the times{Style.RESET_ALL}\n')
            continue
        # Checks if username already exists
        try:
            if bool( rq.get(BASE_URL+f'exists/{username}/',proxies=PROXIES).json()['exists'] ):
                print(f'{Fore.RED}{Style.BRIGHT}ERROR: Username not available{Style.RESET_ALL}\n')
                continue
        # If the site is down or we dont have a connection
        except rq.exceptions.ConnectionError:
            print(f'{Fore.RED}{Style.BRIGHT}FATAL: Either the server is down, or you don\'t have an internet connection, please try again later{Style.RESET_ALL}\n')
            sys.exit()
        
        # Send req
        try:
            body = {'username':username, 'password':password}
            response = rq.post(BASE_URL+'signup/', body, proxies=PROXIES).json()
            # Checks if there was an error
            if response.get('error'):
                print(f'{Fore.RED}{Style.BRIGHT}SIGNUP ERROR: {response["error"]}{Style.RESET_ALL}\n')
                continue
        # If the site is down or we dont have a connection
        except rq.exceptions.ConnectionError:
            print(f'{Fore.RED}{Style.BRIGHT}FATAL: Either the server is down, or you don\'t have an internet connection, please try again later{Style.RESET_ALL}\n')
            sys.exit()

        # Tells acc has been created
        AUTH = {'username':username, 'password':password}
        print(f'{Style.BRIGHT}@{response["username"]} has been succesfully created and logged in!{Style.RESET_ALL}')
        break














# ---------------------------------------------------------------------------------------------------- LOGIN ----------------------------------------------------------------------------------------------------

elif signup_or_login in ['1','login']:
    while True:
        print(f'{Style.BRIGHT}Please enter your login details:{Style.RESET_ALL}\n')
        username = input(f'{Style.BRIGHT}username:{Style.RESET_ALL} ').lower()
        password = getpass(f'{Style.BRIGHT}password:{Style.RESET_ALL} ')

        cls()
        body = {'username':username, 'password':password}
        # Sends the query
        try:
            body = {'username':username, 'password':password}
            response = rq.post(BASE_URL+'login/', body, proxies=PROXIES).json()
            # Checks if there was an error
            if response.get('error'):
                print(f'{Fore.RED}{Style.BRIGHT}LOGIN ERROR: {response["error"]}{Style.RESET_ALL}\n')
                continue
            # Checks if the password is correct
            if not bool(response['matching']):
                print(f'{Fore.RED}{Style.BRIGHT}ERROR: The username and/or password are incorrect, please try again{Style.RESET_ALL}\n')
                continue
        # If the site is down or we dont have a connection
        except rq.exceptions.ConnectionError:
            print(f'{Fore.RED}{Style.BRIGHT}FATAL: Either the server is down, or you don\'t have an internet connection, please try again later{Style.RESET_ALL}\n')
            sys.exit()

        AUTH = {'username':username, 'password':password}
        print(f'{Style.BRIGHT}You have succesfully logged in as @{username} !{Style.RESET_ALL}')
        break














# ---------------------------------------------------------------------------------------------------- HOME ----------------------------------------------------------------------------------------------------

cls()
while True:
    print(f'{Fore.MAGENTA}{HOME_LOGO}{Fore.RESET}')
    print(tor_text())
    print(f'(Logged in as @{AUTH["username"]})\n\n')
    print(f'{Style.BRIGHT}Where would you like to go?{Style.RESET_ALL}\n')
    print(f'{Fore.CYAN}[1]{Fore.RESET} {Fore.YELLOW}Inbox{Fore.RESET}')
    print(f'{Fore.CYAN}[2]{Fore.RESET} {Fore.YELLOW}Compose a mail{Fore.RESET}')
    print(f'{Fore.CYAN}[3]{Fore.RESET} {Fore.YELLOW}Exit{Fore.RESET}')
    home_chc = input('\n').lower()

    cls()
    if not home_chc in ['1','2','3','inbox','compose a mail','exit']:
        print(f'{Fore.RED}{Style.BRIGHT}ERROR: Please select a valid option{Style.RESET_ALL}\n')
        continue
    if home_chc in ['3','exit']:
        sys.exit()











# ---------------------------------------------------------------------------------------------------- SEND A MSG ----------------------------------------------------------------------------------------------------

    if home_chc in ['2','compose a mail']:

        print(f'{Style.BRIGHT}From:{Style.RESET_ALL} @{AUTH["username"]}\n')
        destination = input(f'{Style.BRIGHT}To:{Style.RESET_ALL} @').lower()
        
        # Checks if the destination and origin is same
        if destination == AUTH['username']:
            cls()
            print(f'{Fore.RED}{Style.BRIGHT}ERROR: You cannot send messages to yourself{Style.RESET_ALL}\n')
            continue

        # Checks if destination exists
        try:
            if not bool( rq.get(BASE_URL+f'exists/{destination}/',proxies=PROXIES).json()['exists'] ):
                cls()
                print(f'{Fore.RED}{Style.BRIGHT}ERROR: @{destination} does NOT exist. Please recheck your spelling{Style.RESET_ALL}\n')
                continue
        # If the site is down or we dont have a connection
        except rq.exceptions.ConnectionError:
            print(f'{Fore.RED}{Style.BRIGHT}FATAL: Either the server is down, or you don\'t have an internet connection, please try again later{Style.RESET_ALL}\n')
            sys.exit()

        print('\n(Please make sure that the header doesn\'t exceed 30 characters or else it will not show to the recipent. Press enter to leave it blank)')
        mail_head = input(f'{Style.BRIGHT}Header:{Style.RESET_ALL} ')
        mail_body = input(f'\n{Style.BRIGHT}Please write the body of the mail:{Style.RESET_ALL}\n\n')

        cls()

        # Sends req
        try:
            body = AUTH.copy()
            body['destination'] = destination
            body['header'] = mail_head
            body['body'] = mail_body
            response = rq.post(BASE_URL+'message/', body, proxies=PROXIES).json()

            # Checks if there was an error
            if response.get('error'):
                print(f'{Fore.RED}{Style.BRIGHT}SENDING MESSAGE ERROR: {response["error"]}{Style.RESET_ALL}\n')
                continue
        # If the site is down or we dont have a connection
        except rq.exceptions.ConnectionError:
            print(f'{Fore.RED}{Style.BRIGHT}FATAL: Either the server is down, or you don\'t have an internet connection, please try again later{Style.RESET_ALL}\n')
            sys.exit()

        # Checks if it was a success
        if response.get('status') == 'success':
            cls()
            print('(Mail was succesfully sent)')




        










# ---------------------------------------------------------------------------------------------------- INBOX ----------------------------------------------------------------------------------------------------

    elif home_chc in ['1','inbox']:
        in_inbox = True
        while in_inbox:
            to_stop_inbox = False

            # Asks the server for our inbox
            try:
                body = AUTH.copy()
                msges = rq.post(BASE_URL+'inbox/', body, proxies=PROXIES).json()            
                # Checks if there was an error
                if msges.get('error'):
                    print(f'{Fore.RED}{Style.BRIGHT}SENDING MESSAGE ERROR: {msges["error"]}{Style.RESET_ALL}\n')
                    continue        
            # If the site is down or we dont have a connection
            except rq.exceptions.ConnectionError:
                print(f'{Fore.RED}{Style.BRIGHT}FATAL: Either the server is down, or you don\'t have an internet connection, please try again later{Style.RESET_ALL}\n')
                sys.exit()
            
            # Checks if we dont have any messages
            if not len(msges):
                print(f'{Style.BRIGHT}There are no unread mails. Please press enter to continue\n{Style.RESET_ALL}')
                input()
                cls()
                in_inbox = False
                continue

            print(f'{Fore.RED}{Style.BRIGHT}WARNING: Mails will be DELETED once you open them{Style.RESET_ALL}\n')
            myTable = PrettyTable( [f'{Fore.CYAN}{x}{Style.RESET_ALL}' for x in ['ID','From','Header']] )

            # Prints the data
            msg_ids = list(msges.keys())
            for msg_id in msges.keys():
                dic = msges[msg_id]
                myTable.add_row( [msg_id,dic['origin'],dic['header']] )
            print(myTable)

            # Gets the id of the message that the user wants to see
            valid_msg_id = False
            while not valid_msg_id:
                inbox_chc = input(f'\n{Style.BRIGHT}Please enter the ID of the mail you want to view or press {Style.RESET_ALL}{Fore.YELLOW}e{Style.RESET_ALL}{Style.BRIGHT} to exit your inbox{Style.RESET_ALL}\n')
                if inbox_chc in msg_ids:
                    valid_msg_id = True
                elif inbox_chc == 'e':
                    valid_msg_id = True
                    to_stop_inbox = True
                else:
                    print(f'{Style.BRIGHT}{Fore.RED}ERROR: Invalid message ID{Style.RESET_ALL}\n')

            # Checks if user wanted to exit inbox
            if to_stop_inbox:
                cls()
                in_inbox = False
                continue

            # Gets the message
            try:
                body = AUTH.copy()
                body['message_id'] = inbox_chc
                msg = rq.post(BASE_URL+'read/', body, proxies=PROXIES).json()            
                # Checks if there was an error
                if msges.get('error'):
                    print(f'{Fore.RED}{Style.BRIGHT}SENDING MESSAGE ERROR: {msges["error"]}{Style.RESET_ALL}\n')
                    continue        
            # If the site is down or we dont have a connection
            except rq.exceptions.ConnectionError:
                print(f'{Fore.RED}{Style.BRIGHT}FATAL: Either the server is down, or you don\'t have an internet connection, please try again later{Style.RESET_ALL}\n')
                sys.exit()


            # Prints the mail
            cls()
            print('(Press enter to continue)')
            print(f'{Style.BRIGHT}FROM:{Style.RESET_ALL} @{msg["origin"]}\n')
            print(f'{Style.BRIGHT}HEADER:{Style.RESET_ALL} {msg["header"]}\n')
            print(f'{Style.BRIGHT}BODY:{Style.RESET_ALL}\n\n{msg["body"]}\n')
            input()
            cls()
            continue






























'''
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
'''



