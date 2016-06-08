import requests
import time
import subprocess
import obd

PARKLOT_HOST = r'https://parklot.herokuapp.com/'
#PARKLOT_HOST = r'http://192.168.11.14:4040/'
VALIDATE_VEH_SERV = r'veh/'
POST_CHECKIN_SERV = r'checkin/'

def get_valid_mvas(vehdata={"veh":[]}):
    print("Posting data to the server for MVA validation ...")
    valid_mvas = []
    requrl = PARKLOT_HOST + VALIDATE_VEH_SERV
    r = requests.post(requrl, vehdata)
    print(r.json())
    valid_mvas = r.json()['veh']
    return valid_mvas

def connect_thru_rfcomm(vehaddr,port="1"):
    try:
        proc = subprocess.Popen(["rfcomm", "connect", "/dev/rfcomm0", vehaddr,port,"&"])
        time.sleep(10)
        print("Slept for 10 secs: Command should have completed")
        return 0
    except:
        return -1


def disconnect_all_rfcomm():
    try:
        proc2 = subprocess.Popen(["rfcomm", "release", "/dev/rfcomm0"])
        time.sleep(5)
        print("Disconnected")
    except:
        pass


def get_vehicle_details(commands=[None]):
    print("Getting vehicle details from OBD")
    responses = []
    if(commands[0] != None):
        conn = obd.OBD("/dev/rfcomm0")
        for command in commands:
            cmd = obd.commands[command]
            resp = conn.query(cmd)
            responses.append((resp.value,resp.unit))
    return responses


def post_checkin(lotid=None,mva=None,miles=None,gas=None):
    if (lotid != None):
        print("Posting checked-in vehicle data ...")
        requrl = PARKLOT_HOST + POST_CHECKIN_SERV
        checkin_data = {'lotid':lotid, 'mva':mva, 'miles':miles, 'gas':gas}
        r = requests.post(requrl, checkin_data)
        print(r.status_code)
        #print(r.json())
        return None

