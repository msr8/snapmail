from colorama import init,Fore,Back,Style
from getpass import getpass
from stuff import LOGO, HOME_LOGO
import requests as rq
import platform as pf
import time as t
import sys
import os
init()

# BASE_URL = 'http://127.0.0.1:5000/'
BASE_URL = 'https://msr8.jprq.io/'


def slow_line_type(to_type):
	for line in to_type.split('\n'):
		print(line)
		t.sleep(0.2)


cls = lambda: os.system('cls' if pf.system()=='Windows' else 'clear')
cls()	















slow_line_type(f'{Fore.MAGENTA}{LOGO}{Fore.RESET}')
print('\n')
while True:
	print(f'{Style.BRIGHT}Welcome to Mark\'s services! What would you like to do?{Style.RESET_ALL}\n')
	print(f'{Fore.CYAN}[1]{Fore.RESET} {Fore.YELLOW}Login{Fore.RESET}')
	print(f'{Fore.CYAN}[2]{Fore.RESET} {Fore.YELLOW}Signup{Fore.RESET}')
	print(f'{Fore.CYAN}[3]{Fore.RESET} {Fore.YELLOW}Exit{Fore.RESET}')
	signup_or_login = input('\n').lower()
	if not signup_or_login in ['1','2','3','login','signup','exit']:
		cls()
		print(f'{Fore.RED}{Style.BRIGHT}ERROR: Please select a valid option{Style.RESET_ALL}\n')
		continue
	break

cls()

if signup_or_login in ['3','exit']:
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
			if bool( rq.get(BASE_URL+f'exists/{username}').json()['exists'] ):
				print(f'{Fore.RED}{Style.BRIGHT}ERROR: Username not available{Style.RESET_ALL}\n')
				continue
		# If the site is down or we dont have a connection
		except rq.exceptions.ConnectionError:
			print(f'{Fore.RED}{Style.BRIGHT}FATAL: Either the server is down, or you don\'t have an internet connection, please try again later{Style.RESET_ALL}\n')
			sys.exit()
		
		# Send req
		try:
			body = {'username':username, 'password':password}
			response = rq.post(BASE_URL+'signup', body).json()
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
			response = rq.post(BASE_URL+'login', body).json()
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
			if not bool( rq.get(BASE_URL+f'exists/{destination}').json()['exists'] ):
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
			response = rq.post(BASE_URL+'message', body).json()

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
			print('(Message was succesfully sent)')




		










# ---------------------------------------------------------------------------------------------------- INBOX ----------------------------------------------------------------------------------------------------

	elif home_chc in ['1','inbox']:
		in_inbox = True
		while in_inbox:
			to_stop_inbox = False

			# Asks the server for our inbox
			try:
				body = AUTH.copy()
				msges = rq.post(BASE_URL+'inbox', body).json()			
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
			print(f'{Back.BLACK}{Fore.WHITE}{Style.BRIGHT}S. NO{Style.RESET_ALL}    {Back.BLACK}{Fore.WHITE}{Style.BRIGHT}From{Style.RESET_ALL}    {Back.BLACK}{Fore.WHITE}{Style.BRIGHT}Header{Style.RESET_ALL}\n')

			# Prints the data
			msg_ids = list(msges.keys())
			for msg_id in msges.keys():
				dic = msges[msg_id]
				print(f'{Back.BLACK}{Fore.WHITE}{msg_id}{Style.RESET_ALL}    {Back.BLACK}{Fore.WHITE}{dic["origin"]}{Style.RESET_ALL}    {Back.BLACK}{Fore.WHITE}{dic["header"]}{Style.RESET_ALL}')

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
				msg = rq.post(BASE_URL+'read', body).json()			
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



