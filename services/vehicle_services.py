import requests


def get_valid_mvas(veh_data={"veh":[]}):
    print("Posting data to the server for MVA validation ...")
    r = requests.post("https://parklot.herokuapp.com/veh", vehdata)
    print(r.json())
    nearest_vehicles = r.json()['veh']
