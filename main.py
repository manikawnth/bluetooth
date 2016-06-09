#Test module

from nearest_devices import get_nearest_devices
import services.vehicle_services as VS
import subprocess

LOT_ID = 'B8:27:EB:CD:05:88'
while True:
    # {'00:11:22:33:44:55' : -60 , '00:A1:B2:33:F4:C5' : -30 , 'B8:A1:22:C3:4F:55' : -40}
    print("STEP1 - Scanning for the nearest devices")
    nearest_devices = get_nearest_devices()
    print("nearest devices:",nearest_devices)
    if (len(nearest_devices.keys()) == 0): continue


    #Post the data to the service and get valid MVAs
    # [ {'A0:02:DC:51:49:F9': '068543219'} , {'D0:25:98:BD:C0:3B': '894532103'} ]
    print("STEP2 - Getting valid mvas from service")
    vehdata = {"veh": list(nearest_devices)}
    vehdata['veh'].append('XX:XX:XX:XX:XX:XX')  #always append a dirty one
    nearest_vehicles = VS.get_valid_mvas(vehdata)
    print("nearest vehicles:",nearest_vehicles)
    if (len(nearest_vehicles) == 0): continue

    #Point to the nearest mva
    (nearest_vehicle_id,nearest_vehicle,nearest_frequency) = (None,None,-60)
    print("STEP3 - Filter the nearest vehicle under -60db signal frequency")
    for vehicle in nearest_vehicles:
        for devid in vehicle:
            freq = nearest_devices[devid]
            if (freq > nearest_frequency):
                nearest_vehicle_id = devid
                nearest_vehicle = vehicle[devid]
                nearest_frequency = freq
    print(nearest_vehicle_id,nearest_vehicle,nearest_frequency)
    if (nearest_vehicle_id == None): continue


    #Open an rfcomm socket and connect to the nearest vehicle
    print("STEP4 - Open an rfcomm socket and connect to the nearest one")
    retcode = VS.connect_thru_rfcomm(nearest_vehicle_id,port="1")
    print("RFCOMM return code is:", retcode)


    #Get vehicle diagnostics
    print("STEP5 - Get the vehicle OBD data")
    if (nearest_vehicle_id == 'A0:02:DC:51:49:F9'):
        vehicle_stats = [('6','unit'), ('22345','miles')]
    elif retcode == 0:
        commands = ['FUEL_LEVEL','DISTANCE_SINCE_DTC_CLEAR']
        vehicle_stats = VS.get_vehicle_details(commands)
        print(vehicle_stats)
    else:
        continue


    #Disconnect the rfcomm socket for the current vehicle
    print("STEP6 - Disconnect the RFCOMM socket")
    VS.disconnect_all_rfcomm()


    #post check-in data to vehicle service and store on the server
    print("STEP7 - Posting the checkin data to the server")
    retcode = VS.post_checkin(lotid=LOT_ID,mva=nearest_vehicle,miles=vehicle_stats[1][0],gas=str(round(float(vehicle_stats[0][0]))))
