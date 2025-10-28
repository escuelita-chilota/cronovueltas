# Rui Santos & Sara Santos - Random Nerd Tutorials
# Complete project details at https://RandomNerdTutorials.com/micropython-esp-now-esp32/

import network
import espnow
import time

threshold = -60

# Stats tracking
last_stats_time = time.time()
stats_interval = .1  # Print stats every 10 seconds

# Initialize Wi-Fi in station mode
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(channel=1)  # Set channel explicitly if packets are not received
sta.disconnect()

# Initialize ESP-NOW
e = espnow.ESPNow()
try:
    e.active(True)
except OSError as err:
    print("Failed to initialize ESP-NOW:", err)
    raise

# Sender's MAC address
sender_mac = b'\x30\xae\xa4\x07\x0d\x64'  # Sender MAC

# Add peer (sender) for unicast reliabilityimport 
# You don't need to add peer for broadcast
#try:
#    e.add_peer(sender_mac)
#except OSError as err:
#    print("Failed to add peer:", err)
#    raise

transmiters = {}

print("Listening for ESP-NOW messages...")
while True:
    try:
        # Receive message (host MAC, message, timeout of .1 seconds)
        host, msg = e.recv(25)
        
        #print(e.peers_table)
        
        for peer_mac, (rssi, _time_ms) in e.peers_table.items():
            if rssi < threshold:
                continue
            # TODO: refactor looking for minimal value like:
            # https://github.com/phobos-/PhobosLT/blob/main/lib/LAPTIMER/laptimer.cpp
            #
            if peer_mac in transmiters.keys():
                transmiters[peer_mac].append(rssi)
                if len(transmiters[peer_mac]) >= 6:
                    transmiters[peer_mac].pop(0)
                    if transmiters[peer_mac][0] <= transmiters[peer_mac][1] and \
                        transmiters[peer_mac][1] < transmiters[peer_mac][2] and \
                        transmiters[peer_mac][2] >= transmiters[peer_mac][3] and \
                        transmiters[peer_mac][3] >= transmiters[peer_mac][4]:
                        print(f"lap {peer_mac} at {time.localtime()}")
                        print(transmiters[peer_mac])
            else:
                transmiters[peer_mac] = [rssi]
        
        # # Print stats every 10 seconds
        # if time.time() - last_stats_time >= stats_interval:
        #     #print_stats()
        #     last_stats_time = time.time()
        
    except OSError as err:
        print("Error:", err)
        time.sleep(1)
        
    except KeyboardInterrupt:
        print("Stopping receiver...")
        e.active(False)
        sta.active(False)
        break