import network
import espnow
import time

# Stats tracking
last_stats_time = time.time()
stats_interval = 10  # Print stats every 10 seconds

# Initialize Wi-Fi in station mode
sta = network.WLAN(network.STA_IF)
sta.active(True)
#sta.config(channel=1)  # Set channel explicitly if packets are not delivered
sta.disconnect()

# Initialize ESP-NOW
e = espnow.ESPNow()
try:
    e.active(True)
except OSError as err:
    print("Failed to initialize ESP-NOW:", err)
    raise

# Receiver's MAC address
receiver_mac = b'\xe4e\xb8wT\xec'
#receiver_mac = b'\xff\xff\xff\xff\xff\xff' #broadcast

# Add peer
try:
    e.add_peer(receiver_mac)
except OSError as err:
    print("Failed to add peer:", err)
    raise

def print_stats():
    stats = e.stats()
    print("\nESP-NOW Statistics:")
    print(f"  Packets Sent: {stats[0]}")
    print(f"  Packets Delivered: {stats[1]}")
    print(f"  Packets Dropped (TX): {stats[2]}")
    print(f"  Packets Received: {stats[3]}")
    print(f"  Packets Dropped (RX): {stats[4]}")
    
# Main loop to send messages
while True:
    try:
        # Send the message without acknowledgment
        try:
            e.send(receiver_mac, b'h', False)
            print(f"Ping")
        except OSError as err:
            print(f"Failed to send message (OSError: {err})")
        
        # Print stats every 10 seconds
        if time.time() - last_stats_time >= stats_interval:
            print_stats()
            last_stats_time = time.time()


        # Send every 1/100 seconds.
        # At 180 kph => 50 mps, we should get ~50cm max between samples
        time.sleep(.01)
        
    except OSError as err:
        print("Error:", err)
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("Stopping sender...")
        e.active(False)
        sta.active(False)
        break