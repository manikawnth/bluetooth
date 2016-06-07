
import inquiry_with_rssi as inq


def get_nearest_devices(search_times = 3, unique=True):
    #Inquire rssi 3 times and return the nearest unique devices
    nearest_devices = {}
    print("Scanning all the available bluetooth devices 3 times")
    for i in range(search_times):
        print("Iteration %d" %(i))
        dev = inq.rssi_main()
        for (bdaddr,freq) in dev:
            if (bdaddr in nearest_devices and int(freq) > int(nearest_devices[bdaddr])) or (bdaddr not in nearest_devices):
                nearest_devices[bdaddr] = int(freq)
    return nearest_devices