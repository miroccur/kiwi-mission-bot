import tkinter as tk
import requests
import json
import multiprocessing
import time
import os
import ast
import threading

s=requests.session()
login_state=None
username=None
the_email=None
the_password=None
ifRefill=None
mission=None
stars=None
ib_status=None
bs_status=None
pp_status=None
es_status=None
anubis_status=None
task_id=None
task_timer=None
task_status=None
task_current_star=None
task_id_cycle=None

#function to retrieve task chain information 
def get_mission_status():
	#declaring global variables to store task chain information
	global ib_status
	global bs_status
	global pp_status
	global es_status
	global anubis_status
	#send https request (GET request) to retrieve task chain information, and store them in respective variables
	ib_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=icebreaker").json()
	bs_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=shark").json()
	pp_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=pripyat").json()
	es_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=volcano").json()
	anubis_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=anubis").json()
#init dictionaries for task id, task's remaining time, task's status and task's difficulty
def task_init():
	#declare global variables to store respective information from task chain
	global task_id
	global task_timer
	global task_status
	global task_current_star
	global task_id_cycle
	global task_timer_cycle
	global task_status_cycle
	#dictionary for task id
	task_id = {'North':49,'Bear':51,'Water':59,'Rift':60,'Sword':63,'Meat':64,'Hammer':73,'Bite':74,'Wheel':3,'1986':6,'School':7,'Death':15,'Krakatoa':36,'Fogo':42,'Taupo':37,'Ararat':44,'Sphinx':18,'Amun':27,'Cobra':30,'Oasis':23,}
	#dictionary for task's remaining time
	task_timer = {'North':ib_status['data']['tasks']['2']['49']['remaining_time'],'Bear':ib_status['data']['tasks']['3']['51']['remaining_time'],'Water':ib_status['data']['tasks']['5']['59']['remaining_time'],'Rift':ib_status['data']['tasks']['6']['60']['remaining_time'],'Sword':bs_status['data']['tasks']['2']['63']['remaining_time'], 'Meat':bs_status['data']['tasks']['2']['64']['remaining_time'],'Hammer':bs_status['data']['tasks']['5']['73']['remaining_time'],'Bite':bs_status['data']['tasks']['5']['74']['remaining_time'],'Wheel':pp_status['data']['tasks']['2']['3']['remaining_time'],'1986':pp_status['data']['tasks']['3']['6']['remaining_time'],'School':pp_status['data']['tasks']['3']['7']['remaining_time'],'Death':pp_status['data']['tasks']['6']['15']['remaining_time'],'Krakatoa':es_status['data']['tasks']['3']['36']['remaining_time'],'Fogo':es_status['data']['tasks']['5']['42']['remaining_time'],'Taupo':es_status['data']['tasks']['3']['37']['remaining_time'],'Ararat':es_status['data']['tasks']['5']['44']['remaining_time'],'Sphinx':anubis_status['data']['tasks']['2']['18']['remaining_time'],'Amun':anubis_status['data']['tasks']['5']['27']['remaining_time'],'Cobra':anubis_status['data']['tasks']['6']['30']['remaining_time'],'Oasis':anubis_status['data']['tasks']['3']['23']['remaining_time']}
	#dictionary for task's status
	task_status = {'North':ib_status['data']['tasks']['2']['49']['status'],'Bear':ib_status['data']['tasks']['3']['51']['status'],'Water':ib_status['data']['tasks']['5']['59']['status'],'Rift':ib_status['data']['tasks']['6']['60']['status'],'Sword':bs_status['data']['tasks']['2']['63']['status'], 'Meat':bs_status['data']['tasks']['2']['64']['status'],'Hammer':bs_status['data']['tasks']['5']['73']['status'],'Bite':bs_status['data']['tasks']['5']['74']['status'],'Wheel':pp_status['data']['tasks']['2']['3']['status'],'1986':pp_status['data']['tasks']['3']['6']['status'],'School':pp_status['data']['tasks']['3']['7']['status'],'Death':pp_status['data']['tasks']['6']['15']['status'],'Krakatoa':es_status['data']['tasks']['3']['36']['status'],'Fogo':es_status['data']['tasks']['5']['42']['status'],'Taupo':es_status['data']['tasks']['3']['37']['status'],'Ararat':es_status['data']['tasks']['5']['44']['status'],'Sphinx':anubis_status['data']['tasks']['2']['18']['status'],'Amun':anubis_status['data']['tasks']['5']['27']['status'],'Cobra':anubis_status['data']['tasks']['6']['30']['status'],'Oasis':anubis_status['data']['tasks']['3']['23']['status']}
	#dictionary for task's difficulty
	task_current_star = {'North':ib_status['data']['tasks']['2']['49']['current_star'],'Bear':ib_status['data']['tasks']['3']['51']['current_star'],'Water':ib_status['data']['tasks']['5']['59']['current_star'],'Rift':ib_status['data']['tasks']['6']['60']['current_star'],'Sword':bs_status['data']['tasks']['2']['63']['current_star'], 'Meat':bs_status['data']['tasks']['2']['64']['current_star'],'Hammer':bs_status['data']['tasks']['5']['73']['current_star'],'Bite':bs_status['data']['tasks']['5']['74']['current_star'],'Wheel':pp_status['data']['tasks']['2']['3']['current_star'],'1986':pp_status['data']['tasks']['3']['6']['current_star'],'School':pp_status['data']['tasks']['3']['7']['current_star'],'Death':pp_status['data']['tasks']['6']['15']['current_star'],'Krakatoa':es_status['data']['tasks']['3']['36']['current_star'],'Fogo':es_status['data']['tasks']['5']['42']['current_star'],'Taupo':es_status['data']['tasks']['3']['37']['current_star'],'Ararat':es_status['data']['tasks']['5']['44']['current_star'],'Sphinx':anubis_status['data']['tasks']['2']['18']['current_star'],'Amun':anubis_status['data']['tasks']['5']['27']['current_star'],'Cobra':anubis_status['data']['tasks']['6']['30']['current_star'],'Oasis':anubis_status['data']['tasks']['3']['23']['current_star']}
	#list of tasks in dictionaries' order
	task_id_cycle = list(task_id)

#check if user's character has athlete bonus
def isAthlete():
	#declare the global network session
	global s
	#set up the cookies for auth
	get_mg_token()
	#send https request (GET method) to retrieve character data
	profile_json = s.get('https://wf.my.com/minigames/bp4/info/compose?methods=user.info').json()
	#check whether character has athlete bonus and return the result
	if "athlete" in profile_json['data']['user']['info']['avatar']['skills']:
		return True
	else:
		return False

#function to refill energy
def energy_refill():
	#declare the global network session
	global s
	#set up the cookies for auth
	get_mg_token()
	#send https request (POST method) to refill energy
	refill=s.post('https://wf.my.com/minigames/bp4/user/buy-energy')

#function to write new line at the start of file			
def line_prepender(FileName, line):
	#set up a file session
	with open(FileName, 'r+') as file_session:
		#read existing content
		content = file_session.read()
		#set the pointer back to start
		file_session.seek(0, 0)
		#rewrite the file, add new line then old content
		file_session.write(str(line) + '\n' + str(content))

#function to start the task
def mission_starter(task_name,stars):
	#declare the global network session
	global s
	#set up the request data
	task_info={
		'task_id':str(task_id[task_name]),
		'stars':str(stars)
	}
	#set up the cookies for auth
	get_mg_token()
	#send https request (POST method) to start the task
	start_task = s.post('https://wf.my.com/minigames/bp4/task/start-task',data=task_info).json()

#function to finish the task
def mission_ender(task_name,stars):
	#declare the global network session
	global s
	#set up the request data
	task_ender_info={
		'task_id':str(task_id[task_name]),
		'is_paid':0,
		'stars':str(stars)
	}
	#set up the cookies for auth
	get_mg_token()
	#send https request (POST method) to end the mission
	end_task=s.post('https://wf.my.com/minigames/bp4/task/done-task',data=task_ender_info).json()
	#check if log file exists
	#exists:
	if os.path.isfile(os.path.dirname(os.path.realpath(__file__))+'/'+username+'_log'):
		#if the request was successful
		if end_task['state']=="Success":
			#write the response to log
			line_prepender(os.path.dirname(os.path.realpath(__file__))+'/'+username+'_log', end_task)
	#does not exist:
	else:
		#create file with a session
		file_creation=open(os.path.dirname(os.path.realpath(__file__))+'/'+username+'_log','w+')
		file_creation.close()
		#if the request was successful
		if end_task['state']=="Success":
			#write the response to log
			line_prepender(os.path.dirname(os.path.realpath(__file__))+'/'+username+'_log', end_task)

#function to set up the cookies for auth				
def get_mg_token():
	#declare the global network session
	global s
	#send https request (GET method) to retrieve profile data
	get_token = s.get('https://wf.my.com/minigames/user/info').json()
	#read token from the profile data and set up into the session
	#the token expires after every http/https POST request
	s.cookies['mg_token'] = get_token['data']['token']

#function to login to warface account and switch to login confirmation page
def login(email,password):
	#declare the global network session
	global s
	#declare variables to store login status
	global login_state
	global username
	#set up the headers for login request
	headers = {
			'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, br',
			'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
			'Cache-Control':'max-age=0',
			'Connection':'keep-alive',
			'Content-Type':'application/x-www-form-urlencoded',
			'Cookie':'s=dpr=1; amc_lang=en_US; t_0=1; _ym_isad=1',
			'DNT':'1',
			'Host':'auth-ac.my.com',
			'Origin':'https://wf.my.com',
			'Referer':'https://wf.my.com/kiwi',
			'Upgrade-Insecure-Requests':'1',
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
			}
	while True:
		try:
			#set up the login data
			login_data = {
					'email':email,
					'password':password,
					'continue':'https://account.my.com/login_continue/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F',
					'failure':'https://account.my.com/login/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F',
					'nosavelogin':'0'
				}
			#send https (POST and GET method) request to login
			s.post('https://auth-ac.my.com/auth',headers=headers,data=login_data)
			s.get('https://auth-ac.my.com/sdc?from=https%3A%2F%2Fwf.my.com')
			s.get('https://wf.my.com/')
			#set up the cookies for auth
			get_mg_token()
			#check login state and kiwi access
			user_check_json = s.get('https://wf.my.com/minigames/bp4/info/compose?methods=user.info').json()
			#login attempt was successful and has kiwi access
			if user_check_json['data']['user']['info']['status']=='member':
				login_state='yes'
				username=user_check_json['data']['user']['info']['username']
			#login attempt was successful but no kiwi access
			elif user_check_json['data']['user']['info']['status']=='guest':
				login_state='guest'
				username=user_check_json['data']['user']['info']['username']
			#login attempt failed
			elif user_check_json['data']['user']['info']['status']=='no_auth':
				login_state='no_auth'
		except(KeyError,ValueError,TypeError,requests.exceptions.ChunkedEncodingError,json.decoder.JSONDecodeError,requests.exceptions.ConnectionError,requests.exceptions.TooManyRedirects):
			continue
		break


class main(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		#init the frame var
		self._frame = None
		#start the app with login page
		self.switch_frame(login_page)
	#set up framw switching function
	def switch_frame(self, frame_class):
		#destroys current frame and replaces it with a new one
		new_frame = frame_class(self)
		#check current frame
		if self._frame is not None:
			self._frame.destroy()
		self._frame = new_frame
		#display new targetted frame
		self._frame.pack()

#set up login page
class login_page(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		#declare the global network session
		global s
		#declare global variables to store login status
		global login_state
		global username
		global email
		global password
		#set up a function to login and continue to next page
		def next_page(email,password):
			#declare the global network session
			global s
			#declare global variables to store login status
			global login_state
			global username
			global the_email
			global the_password
			#store email and password in global variables
			the_email=email
			the_password=password
			#set up the login process
			login_process=multiprocessing.Process(target=login(email,password))
			#login
			login_process.start()
			login_process.join()
			master.switch_frame(confirm_page)
		#set up descriptive page label
		the_label=tk.Label(self,text="K.I.W.I. Mission Automator",font=("San Francisco",20))
		the_label.grid(row=0)
		nevi_label=tk.Label(self,text="Please login to your Warface account (my.com based)",font=("San Francisco",16))
		nevi_label.grid(row=1)
		#set up login info label
		email_label=tk.Label(self,text="Email or mobile phone number:")
		email_label.grid(row=2,sticky="W")
		pw_label=tk.Label(self,text="Password:")
		pw_label.grid(row=3,sticky="W")
		#set up entry box
		get_email=tk.StringVar()
		get_password=tk.StringVar()
		email_entry=tk.Entry(self,textvariable=get_email)
		email_entry.grid(row=2,sticky="E")
		pw_entry=tk.Entry(self,show="*",textvariable=get_password)
		pw_entry.grid(row=3,sticky="E")
		#set up quit and login button
		quit_button=tk.Button(self,text="Quit")
		quit_button.config(width=8)
		quit_button.config(command=lambda:exit())
		quit_button.grid(row=5,column=0,sticky="W",padx=80)
		login_button=tk.Button(self,text="Login")
		login_button.config(width=8)
		login_button.config(command=lambda:next_page(get_email.get(),get_password.get()))
		login_button.grid(row=5,column=0,sticky="E",padx=80)

#set up login confirmation page
class confirm_page(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		#declare the global network session
		global s
		#declare global variables to show login status
		global login_state
		global username
		#check login state and kiwi access
		if login_state=='yes':
			#set up state label
			the_label=tk.Label(self,text="You are logged in as "+username+".")
			the_label.grid(row=0)
			#set up choice button
			continue_button=tk.Button(self,text="Continue",width=6)
			continue_button.config(command=lambda:master.switch_frame(config_page))
			continue_button.grid(row=1,sticky='E',padx=10)
			return_button=tk.Button(self,text="Log off",width=6)
			return_button.config(command=lambda:master.switch_frame(login_page))
			return_button.grid(row=1,sticky='W',padx=10)
		elif login_state=='no_auth':
			#set up state label
			the_label=tk.Label(self,text="Your login information were incorrect.")
			the_label.grid(row=0)
			#set up the button
			return_button=tk.Button(self,text="Retry",width=6)
			return_button.config(command=lambda:master.switch_frame(login_page))
			return_button.grid(row=1)
		else:
			#set up state label
			the_label=tk.Label(self,text="The account you logged in, "+str(username)+" does not have K.I.W.I. access.")
			the_label.grid(row=0)
			#set up the button
			return_button=tk.Button(self,text="Retry",width=6)
			return_button.config(command=lambda:master.switch_frame(login_page))
			return_button.grid(row=1)
#set up config page1
class config_page(tk.Frame):
	def __init__(self, master):
		global mission
		get_mission=tk.StringVar()
		get_mission.set('0')
		def config_mission():
			global mission
			mission=get_mission.get()
			master.switch_frame(config2_page)
		tk.Frame.__init__(self, master)
		#set up the label
		the_label=tk.Label(self,text="Please choose the mission",font=("San Francisco",16))
		the_label.grid(row=0,columnspan=4)
		#set up the radio buttons
		#Icebreaker
		North=tk.Radiobutton(self,text="North",variable=get_mission,value="North")
		North.grid(row=1,column=0,sticky="W")
		Bear=tk.Radiobutton(self,text="Bear",variable=get_mission,value="Bear")
		Bear.grid(row=1,column=1,sticky="W")
		Water=tk.Radiobutton(self,text="Water",variable=get_mission,value="Water")
		Water.grid(row=1,column=2,sticky="W")
		Rift=tk.Radiobutton(self,text="Rift",variable=get_mission,value="Rift")
		Rift.grid(row=1,column=3,sticky="W")
		#Black Shark
		Sword=tk.Radiobutton(self,text="Sword",variable=get_mission,value="Sword")
		Sword.grid(row=2,column=0,sticky="W")
		Meat=tk.Radiobutton(self,text="Meat",variable=get_mission,value="Meat")
		Meat.grid(row=2,column=1,sticky="W")
		Hammer=tk.Radiobutton(self,text="Hammer",variable=get_mission,value="Hammer")
		Hammer.grid(row=2,column=2,sticky="W")
		Bite=tk.Radiobutton(self,text="Bite",variable=get_mission,value="Bite")
		Bite.grid(row=2,column=3,sticky="W")
		#Pripyat
		Wheel=tk.Radiobutton(self,text="Wheel",variable=get_mission,value="Wheel")
		Wheel.grid(row=3,column=0,sticky="W")
		Pripyat1986=tk.Radiobutton(self,text="1986",variable=get_mission,value="1986")
		Pripyat1986.grid(row=3,column=1,sticky="W")
		School=tk.Radiobutton(self,text="School",variable=get_mission,value="School")
		School.grid(row=3,column=2,sticky="W")
		Death=tk.Radiobutton(self,text="Death",variable=get_mission,value="Death")
		Death.grid(row=3,column=3,sticky="W")
		#Earth Shaker
		Krakatoa=tk.Radiobutton(self,text="Krakatoa",variable=get_mission,value="Krakatoa")
		Krakatoa.grid(row=4,column=0,sticky="W")
		Fogo=tk.Radiobutton(self,text="Fogo",variable=get_mission,value="Fogo")
		Fogo.grid(row=4,column=1,sticky="W")
		Taupo=tk.Radiobutton(self,text="Taupo",variable=get_mission,value="Taupo")
		Taupo.grid(row=4,column=2,sticky="W")
		Ararat=tk.Radiobutton(self,text="Ararat",variable=get_mission,value="Ararat")
		Ararat.grid(row=4,column=3,sticky="W")
		#Anubis
		Sphinx=tk.Radiobutton(self,text="Sphinx",variable=get_mission,value="Sphinx")
		Sphinx.grid(row=5,column=0,sticky="W")
		Amun=tk.Radiobutton(self,text="Amun",variable=get_mission,value="Amun")
		Amun.grid(row=5,column=1,sticky="W")
		Cobra=tk.Radiobutton(self,text="Cobra",variable=get_mission,value="Cobra")
		Cobra.grid(row=5,column=2,sticky="W")
		Oasis=tk.Radiobutton(self,text="Oasis",variable=get_mission,value="Oasis")
		Oasis.grid(row=5,column=3,sticky="W")
		#setup button
		continue_button=tk.Button(self,text="Continue",width=8)
		continue_button.config(command=lambda:config_mission())
		continue_button.grid(row=6,column=0,columnspan=4)

#set up config page2
class config2_page(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		global stars
		global mission
		get_stars=tk.IntVar()
		def config2_mission():
			global stars
			stars=get_stars.get()
			master.switch_frame(config3_page)
		#set up the label
		the_label=tk.Label(self,text="Mission: "+mission+"\nPlease choose the mission level",font=("San Francisco",16))
		the_label.grid(row=0,columnspan=3)
		#set up the radio buttons
		one=tk.Radiobutton(self,text="1 star",variable=get_stars,value=1)
		one.grid(row=1,column=0)
		two=tk.Radiobutton(self,text="2 stars",variable=get_stars,value=2)
		two.grid(row=1,column=1)
		three=tk.Radiobutton(self,text="3 stars",variable=get_stars,value=3)
		three.grid(row=1,column=2)
		#set up the bottons
		continue_button=tk.Button(self,text="Continue",width=10)
		continue_button.config(command=lambda:config2_mission())
		continue_button.grid(row=2,column=0,columnspan=3,sticky='E',padx=12)
		goback_button=tk.Button(self,text="Change mission",width=10)
		goback_button.config(command=lambda:master.switch_frame(config_page))
		goback_button.grid(row=2,column=0,columnspan=3,sticky='W',padx=12)
		
#set up config page3
class config3_page(tk.Frame):
	def __init__(self, master):
		tk.Frame.__init__(self, master)
		global ifRefill
		global mission
		global stars
		get_refill=tk.IntVar()
		get_refill.set(3)
		def config3_mission():
			global ifRefill
			result=get_refill.get()
			if result==0:
				ifRefill=True
			elif result==1:
				ifRefill=False
			master.switch_frame(dashboard)
		#set up the label
		the_label=tk.Label(self,text="Mission: "+mission+"\nLevel: "+str(stars)+"\nDo you want to refill energy automatically \nwith Battle Points when it's insufficient?",font=("San Francisco",16))
		the_label.grid(row=0,columnspan=2)
		#set up radiobuttons
		yes_button=tk.Radiobutton(self,text="Yes",value=0,variable=get_refill)
		yes_button.grid(row=1,column=0)
		no_button=tk.Radiobutton(self,text="No",value=1,variable=get_refill)
		no_button.grid(row=1,column=1)
		#set up the button
		continue_button=tk.Button(self,text="Start",width=9)
		continue_button.config(command=lambda:config3_mission())
		continue_button.grid(row=2,column=1)
		goback_button=tk.Button(self,text="Reconfigure",width=9)
		goback_button.config(command=lambda:master.switch_frame(config_page))
		goback_button.grid(row=2,column=0)

class dashboard(tk.Frame):
	def __init__(self,master):
		tk.Frame.__init__(self,master)
		global s
		global ifRefill
		global mission
		global stars
		global ib_status
		global bs_status
		global pp_status
		global es_status
		global anubis_status
		global task_id
		global task_timer
		global task_status
		global task_current_star
		global task_id_cycle
		def farmStarter():
			global stars
			global mission
			global ifRefill
			global current_task
			global ib_status
			global bs_status
			global pp_status
			global es_status
			global anubis_status
			global task_id
			global task_timer
			global task_status
			global task_current_star
			global task_id_cycle
			global task_timer_cycle
			global task_status_cycle
			while True:
				try:
					get_mission_status()
					task_init()
					for counter in range(20):
						if task_timer[task_id_cycle[counter]] == 0 and task_status[task_id_cycle[counter]] == 'open':
							pass
						else:
							if task_timer[task_id_cycle[counter]] != 0:
								sleeper = int(task_timer[task_id_cycle[counter]])
								time.sleep(sleeper)
								mission_ender(task_id_cycle[counter], task_current_star[task_id_cycle[counter]])
								break
							elif task_timer[task_id_cycle[counter]] == 0 and task_status[task_id_cycle[counter]] == "progress":
								mission_ender(task_id_cycle[counter],task_current_star[task_id_cycle[counter]])
								break
					while True:
						get_mission_status()
						task_init()
						profile_json = s.get('https://wf.my.com/minigames/bp4/info/compose?methods=user.info').json()
						energy_count = int(profile_json['data']['user']['info']['cheerfulness'])
						if task_timer[mission] == 0 and task_status[mission]=='open':
							if ifRefill:
								if str(stars)=="3":
									if isAthlete():
										if energy_count<10:
												energy_refill()
									else:
										if energy_count<15:
												energy_refill()
								elif str(stars)=="2":
									if isAthlete():
										if energy_count<7:
											energy_refill()
									else:
										if energy_count<12:
											energy_refill()
								elif str(stars)=="1":
									if isAthlete():
										if energy_count<3:
											energy_refill()
									else:
										if energy_count<8:
											energy_refill()
							mission_starter(mission, stars)
						elif task_timer[mission] == 0 and task_status[mission] == 'progress':
							mission_ender(mission, stars)
						time.sleep(5)
				except(KeyError,ValueError,TypeError,requests.exceptions.ChunkedEncodingError,json.decoder.JSONDecodeError,requests.exceptions.ConnectionError,requests.exceptions.ProxyError):
					login(the_email,the_password)
					continue
				break
		#set up canvas updater
		def canvasUpdater():
			while True:
				canvas.delete("all")
				reward_list=[]
				reward_category={}
				if os.path.isfile(os.path.dirname(os.path.realpath(__file__))+'/'+username+'_log'):
					log_session=open(os.path.dirname(os.path.realpath(__file__))+'/'+username+'_log',"r")
					log_content=log_session.readlines()
					for i in range(len(log_content)):
						log_content[i]=log_content[i].replace("'","\"")
						log_json=ast.literal_eval(log_content[i])
						if log_json["data"]["result"]=="success":
							reward_list.append(log_json['data']['rewards']['reward']['item']['ext_name'])
						else:
							continue
					for x in range(len(reward_list)):
						if reward_list[x] not in reward_category:
							reward_category.update({reward_list[x]:1})
						else:
							reward_category.update({reward_list[x]:reward_category[reward_list[x]]+1})
					reward_category_list=list(reward_category)
					for y in range(len(reward_category)):
						temp=(y+1)*20
						canvas.create_text((20,temp),text=reward_category_list[y]+": "+str(reward_category[reward_category_list[y]]),anchor="w")
				else:
					pass
				time.sleep(60)
		def mission_check(mission,stars):
			if stars==1:
				difficulty="1 star"
			elif stars==2:
				difficulty="2 stars"
			elif stars==3:
				difficulty="3 stars"
			mission_label=tk.Label(self,text=mission+", "+difficulty,font=("San Francisco",18))
			mission_label.grid(row=1,sticky="E",columnspan=2,padx=20)
		#function to check if the program is actively farming
		def status_check():
			while True:
				try:
					if farm_process.is_alive():
						status_label=tk.Label(self,text="Status: active",font=("San Francisco",18))
						status_label.grid(row=1,sticky="W",columnspan=2,padx=20)
					else:
						status_label=tk.Label(self,text="Status: inactive",font=("San Francisco",18))
						status_label.grid(row=1,sticky="W",columnspan=2,padx=20)
					time.sleep(1)
				except:
					continue
		farm_process=multiprocessing.Process(target=farmStarter)
		farm_process.start()
		status_check_process=threading._start_new_thread(status_check,())
		def goodbye():
			farm_process.terminate()
			exit()
		def reconfig():
			farm_process.terminate()
			master.switch_frame(config_page)
		#init the thread for mission check
		mission_thread=threading._start_new_thread(mission_check,(mission,stars))
		#set up the label
		the_label=tk.Label(self,text="Dashboard",font=("San Francisco",20))
		the_label.grid(row=0,columnspan=2)
		reward_label=tk.Label(self,text="Rewards:",font=("San Francisco",16))
		reward_label.grid(row=2,column=0,sticky="W",padx=10)
		#set up a canvas
		canvas=tk.Canvas(self)
		canvas.grid(row=3,column=0)
		canvas_thread=threading._start_new_thread(canvasUpdater,())
		#set up buttons
		start_button=tk.Button(self,text="Reconfigure",command=lambda:reconfig(),width=9)
		start_button.grid(row=3,column=1,sticky="N",padx=10,pady=50)
		stop_button=tk.Button(self,text="Stop",command=lambda:goodbye(),width=9)
		stop_button.grid(row=3,column=1,padx=10,pady=50)



app = main()
app.title("K.I.W.I. Mission Automator")
app.mainloop()
