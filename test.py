#Test moduel
import inquiry_with_rssi as inq
import requests

nearest_dev = {}
#Inquire rssi 3 times and store the nearest devices
print("Scanning nearest bluetooth devices 3 times")
for i in range(3):
    print("Iteration %d" %(i))
    dev = inq.rssi_main()
    for (bdaddr,freq) in dev:
        if (bdaddr in nearest_dev and int(freq) > int(nearest_dev[bdaddr])) or (bdaddr not in nearest_dev):
            nearest_dev[bdaddr] = int(freq)

print(nearest_dev)

#Post the data to the service and get valid MVAs
print("Posting data to the server for MVA validation ...")
vehdata = {"veh":list(nearest_dev)}
r = requests.post("https://parklot.herokuapp.com/veh",vehdata)
print(r.json())            

