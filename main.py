#Test module

from nearest_devices import get_nearest_devices
import services.vehicle_services as VS
import subprocess


# {'00:11:22:33:44:55' : -60 , '00:A1:B2:33:F4:C5' : -30 , 'B8:A1:22:C3:4F:55' : -40}
print("STEP1 - Scanning for the nearest devices")
nearest_devices = get_nearest_devices()


#Post the data to the service and get valid MVAs
# [ {'A0:02:DC:51:49:F9': '068543219'} , {'D0:25:98:BD:C0:3B': '894532103'} ]
print("STEP2 - Getting valid mvas from service")
vehdata = {"veh": list(nearest_devices)}
nearest_vehicles = VS.get_valid_mvas(vehdata)


#Point to the nearest mva
(nearest_vehicle,nearest_frequency) = (None,-60)
print("STEP3 - Filter the nearest vehicle under -60db signal frequency")
for vehicle in nearest_vehicles:
    for devid in vehicle:
        freq = nearest_devices[devid]
        if (freq > nearest_frequency):
            nearest_vehicle = vehicle
            nearest_frequency = freq
print(nearest_vehicle,nearest_frequency)


#Open an rfcomm socket and connect to the nearest vehicle
print("STEP4 - Open an rfcomm socket and connect to the nearest one")
retcode = VS.connect_trhu_rfcomm(nearest_vehicle,port="1")


#Get vehicle diagnostics 
print("STEP5 - Get the vehicle OBD data")
if retcode == 0:
    commands = ['FUEL_LEVEL','DISTANCE_SINCE_DTC_CLEAR']
    responses = VS.get_vehicle_details(commands)
    print(responses)
else:
    pass


#Disconnect the rfcomm socket for the current vehicle
print("STEP6 - Disconnect the RFCOMM socket")
VS.disconnect_all_rfcomm()


