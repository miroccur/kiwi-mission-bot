 #! /usr/bin/env python3

import sys
import time
import signal
import requests
import json
import getpass

s = requests.Session()
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
task_timer_cycle=None
task_status_cycle=None

# Login credentials request
email = input("Email: ")
password = getpass.getpass("Password: ")
# Login credentials request

def login():
	# Base header
	payload = {
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'en-US,en;q=0.9,it;q=0.8',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Content-Type':'application/x-www-form-urlencoded',
		'Cookie':'s=dpr=1; amc_lang=en_US; t_0=1; _ym_isad=1',
		'DNT':'1',
		'Host':'auth-ac.my.com',
		'Origin':'https://wf.my.com',
		'Referer':'https://wf.my.com/kiwi',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
		}
	login_data = {
		'email':email,
		'password':password,
		'continue':'https://account.my.com/login_continue/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F',
		'failure':'https://account.my.com/login/?continue=https%3A%2F%2Faccount.my.com%2Fprofile%2Fuserinfo%2F',
		'nosavelogin':'0'
		}
	while True:
		try: 
			s.post('https://auth-ac.my.com/auth',headers=payload,data=login_data)
			s.get('https://auth-ac.my.com/sdc?from=https%3A%2F%2Fwf.my.com')
			s.get('https://wf.my.com/')  
			get_token = s.get('https://wf.my.com/minigames/user/info').json()
			s.cookies['mg_token'] = get_token['data']['token']
			s.cookies['cur_language'] = 'en'
		except:
			continue
		break
		
def get_mg_token():
	get_token = s.get('https://wf.my.com/minigames/user/info').json()
	s.cookies['mg_token'] = get_token['data']['token']
	
def isAthlete():
	profile_json = s.get('https://wf.my.com/minigames/bp4/info/compose?methods=user.info').json()
	if "athlete" in profile_json['data']['user']['info']['avatar']['skills']:
		return True
	else:
		return False
	
def get_mission_status():
	global ib_status
	global bs_status
	global pp_status
	global es_status
	global anubis_status
	ib_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=icebreaker").json()
	bs_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=shark").json()
	pp_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=pripyat").json()
	es_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=volcano").json()
	anubis_status = s.get("https://wf.my.com/minigames/bp4/info/tasks?chain=anubis").json()

def task_init():
	global task_id
	global task_timer
	global task_status
	global task_current_star
	global task_id_cycle
	global task_timer_cycle
	global task_status_cycle
	task_id = {'North':49,'Bear':51,'Water':59,'Rift':60,'Sword':63,'Meat':64,'Hammer':73,'Bite':74,'Wheel':3,'1986':6,'School':7,'Death':15,'Krakatoa':36,'Fogo':42,'Taupo':37,'Ararat':44,'Sphinx':18,'Amun':27,'Cobra':30,'Oasis':23,}
	task_timer = {'North':ib_status['data']['tasks']['2']['49']['remaining_time'],'Bear':ib_status['data']['tasks']['3']['51']['remaining_time'],'Water':ib_status['data']['tasks']['5']['59']['remaining_time'],'Rift':ib_status['data']['tasks']['6']['60']['remaining_time'],'Sword':bs_status['data']['tasks']['2']['63']['remaining_time'], 'Meat':bs_status['data']['tasks']['2']['64']['remaining_time'],'Hammer':bs_status['data']['tasks']['5']['73']['remaining_time'],'Bite':bs_status['data']['tasks']['5']['74']['remaining_time'],'Wheel':pp_status['data']['tasks']['2']['3']['remaining_time'],'1986':pp_status['data']['tasks']['3']['6']['remaining_time'],'School':pp_status['data']['tasks']['3']['7']['remaining_time'],'Death':pp_status['data']['tasks']['6']['15']['remaining_time'],'Krakatoa':es_status['data']['tasks']['3']['36']['remaining_time'],'Fogo':es_status['data']['tasks']['5']['42']['remaining_time'],'Taupo':es_status['data']['tasks']['3']['37']['remaining_time'],'Ararat':es_status['data']['tasks']['5']['44']['remaining_time'],'Sphinx':anubis_status['data']['tasks']['2']['18']['remaining_time'],'Amun':anubis_status['data']['tasks']['5']['27']['remaining_time'],'Cobra':anubis_status['data']['tasks']['6']['30']['remaining_time'],'Oasis':anubis_status['data']['tasks']['3']['23']['remaining_time']}
	task_status = {'North':ib_status['data']['tasks']['2']['49']['status'],'Bear':ib_status['data']['tasks']['3']['51']['status'],'Water':ib_status['data']['tasks']['5']['59']['status'],'Rift':ib_status['data']['tasks']['6']['60']['status'],'Sword':bs_status['data']['tasks']['2']['63']['status'], 'Meat':bs_status['data']['tasks']['2']['64']['status'],'Hammer':bs_status['data']['tasks']['5']['73']['status'],'Bite':bs_status['data']['tasks']['5']['74']['status'],'Wheel':pp_status['data']['tasks']['2']['3']['status'],'1986':pp_status['data']['tasks']['3']['6']['status'],'School':pp_status['data']['tasks']['3']['7']['status'],'Death':pp_status['data']['tasks']['6']['15']['status'],'Krakatoa':es_status['data']['tasks']['3']['36']['status'],'Fogo':es_status['data']['tasks']['5']['42']['status'],'Taupo':es_status['data']['tasks']['3']['37']['status'],'Ararat':es_status['data']['tasks']['5']['44']['status'],'Sphinx':anubis_status['data']['tasks']['2']['18']['status'],'Amun':anubis_status['data']['tasks']['5']['27']['status'],'Cobra':anubis_status['data']['tasks']['6']['30']['status'],'Oasis':anubis_status['data']['tasks']['3']['23']['status']}
	task_current_star = {'North':ib_status['data']['tasks']['2']['49']['current_star'],'Bear':ib_status['data']['tasks']['3']['51']['current_star'],'Water':ib_status['data']['tasks']['5']['59']['current_star'],'Rift':ib_status['data']['tasks']['6']['60']['current_star'],'Sword':bs_status['data']['tasks']['2']['63']['current_star'], 'Meat':bs_status['data']['tasks']['2']['64']['current_star'],'Hammer':bs_status['data']['tasks']['5']['73']['current_star'],'Bite':bs_status['data']['tasks']['5']['74']['current_star'],'Wheel':pp_status['data']['tasks']['2']['3']['current_star'],'1986':pp_status['data']['tasks']['3']['6']['current_star'],'School':pp_status['data']['tasks']['3']['7']['current_star'],'Death':pp_status['data']['tasks']['6']['15']['current_star'],'Krakatoa':es_status['data']['tasks']['3']['36']['current_star'],'Fogo':es_status['data']['tasks']['5']['42']['current_star'],'Taupo':es_status['data']['tasks']['3']['37']['current_star'],'Ararat':es_status['data']['tasks']['5']['44']['current_star'],'Sphinx':anubis_status['data']['tasks']['2']['18']['current_star'],'Amun':anubis_status['data']['tasks']['5']['27']['current_star'],'Cobra':anubis_status['data']['tasks']['6']['30']['current_star'],'Oasis':anubis_status['data']['tasks']['3']['23']['current_star']}
	task_id_cycle = list(task_id)
	task_timer_cycle = list(task_timer)
	task_status_cycle = list(task_status)
	

#Class for color and text customization
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def signal_handler(signal, frame):
	print ('\n'+bcolors.WARNING+"K.I.W.I. Mission Farming Bot was interrupted!"+bcolors.ENDC)
	sys.exit(0)


print (bcolors.OKGREEN+bcolors.HEADER+"\nK.I.W.I. Mission Farming Bot"+bcolors.ENDC)

#LOGIN AND USER CHECK
login()
user_check_json = s.get('https://wf.my.com/minigames/bp4/info/compose?methods=user.info').json()
try:
	print ("Logged in as {}".format(user_check_json['data']['user']['info']['username']))
except KeyError:
	print ("Login failed.")
	sys.exit(0)
	
#GET MISSION PARAMETERS FROM USER INPUT
mission_name = input("Please input the name of mission you want to farm:\n")
mission_level = input("On what level do you want to farm the mission? (1\\2\\3)\n")
ifRefill = None
while ifRefill != 'y' and ifRefill != 'n':
	ifRefill = input("Do you want to refill energy with Battle Points when it's insufficient? (y/n)\n")

#SET PARAMETERS FOR MISSIONS
get_mission_status()
task_init()
mission_para = {
	'task_id':str(task_id[mission_name]),
	'stars':str(mission_level)
	}
mission_finisher_para = {
	'task_id':str(task_id[mission_name]),
	'is_paid':0,
	'stars':str(mission_level)
}

get_mission_status()
task_init()

#CHECK IF AN ACTIVE MISSION IS IN PROGRESS
for counter in range(20):
	if task_timer[task_timer_cycle[counter]] == 0 and task_status[task_status_cycle[counter]] == 'open':
		print (task_timer_cycle[counter])
		print (" is not active\n")
		continue
	else:
		if task_timer[task_timer_cycle[counter]] != 0:
			sleeper = int(task_timer[task_timer_cycle[counter]])
			temp_mission_finisher_para = {
				'task_id':str(task_id[task_timer_cycle[counter]]),
				'is_paid':0,
				'stars':str(task_current_star[task_timer_cycle[counter]])
			}
			print("An active mission is in progress, farming will start after finishing the mission")
			time.sleep(sleeper)
			get_mg_token()
			temp_mission_ender = s.post('https://wf.my.com/minigames/bp4/task/done-task',data=temp_mission_finisher_para)
			break
		elif task_timer[task_timer_cycle[counter]] == 0 and task_status[task_status_cycle[counter]] == "progress":
			temp_mission_finisher_para = {
				'task_id':str(task_id[task_timer_cycle[counter]]),
				'is_paid':0,
				'stars':str(task_current_star[task_timer_cycle[counter]])
			}
			get_mg_token()
			temp_mission_ender = s.post('https://wf.my.com/minigames/bp4/task/done-task',data=temp_mission_finisher_para)
			break

while True:
	get_mission_status()
	task_init()
	profile_json = s.get('https://wf.my.com/minigames/bp4/info/compose?methods=user.info').json()
	energy_count = int(profile_json['data']['user']['info']['cheerfulness'])
	if task_timer[mission_name] == 0 and task_status[mission_name]=='open':
			if ifRefill:
				if str(mission_level)=="3":
					if isAthlete():
						if energy_count<10:
							get_mg_token()
							energy_restoration = s.post('https://wf.my.com/minigames/bp4/user/buy-energy')
					else:
						if energy_count<15:
							get_mg_token()
							energy_restoration = s.post('https://wf.my.com/minigames/bp4/user/buy-energy')
				elif str(mission_level)=="2":
					if isAthlete():
						if energy_count<7:
							get_mg_token()
							energy_restoration = s.post('https://wf.my.com/minigames/bp4/user/buy-energy')
					else:
						if energy_count<12:
							get_mg_token()
							energy_restoration = s.post('https://wf.my.com/minigames/bp4/user/buy-energy')
				elif str(mission_level)=="1":
					if isAthlete():
						if energy_count<3:
							get_mg_token()
							energy_restoration = s.post('https://wf.my.com/minigames/bp4/user/buy-energy')
					else:
						if energy_count<8:
							get_mg_token()
							energy_restoration = s.post('https://wf.my.com/minigames/bp4/user/buy-energy')
			get_mg_token()
			mission_starter = s.post('https://wf.my.com/minigames/bp4/task/start-task',data=mission_para)
			print("\nMission restarted\n")
	elif task_timer[mission_name] == 0 and task_status[mission_name] == 'progress':
		get_mg_token()
		mission_ender = s.post('https://wf.my.com/minigames/bp4/task/done-task',data=mission_finisher_para)
		print('\nMission finished\n')
	time.sleep(60)
		
print ("\nUnexpected exit out of the while.")
