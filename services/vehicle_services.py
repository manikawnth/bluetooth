import requests
import time
import subprocess
import obd

PARKLOT_HOST = 'https://parklot.herokuapp.com/'
VALIDATE_VEH_SERV = 'veh/'

def get_valid_mvas(vehdata={"veh":[]}):
    print("Posting data to the server for MVA validation ...")
    requrl = PARKLOT_HOST + VALIDATE_VEH_SERV
    r = requests.post(requrl, vehdata)
    print(r.json())
    nearest_vehicles = r.json()['veh']
    return nearest_vehicles

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

def get_vehicle_details(commands=[None]):
    responses = []
    if(commands[0] != None):
        conn = obd.OBD("/dev/rfcomm0")
        for command in commands:
            cmd = obd.commands[command]
            resp = conn.query(cmd)
            responses.append((resp.value,resp.unit))
    return responses


