import requests

import subprocess
import re

from threading import Thread
from queue import Queue



commande_sortie = subprocess.run(["arp", "-a"], capture_output = True)
adresses_ip = re.findall("\d+\.\d+\.\d+\.\d+", str(commande_sortie))
adresses_ip = [x for x in adresses_ip if not x.startswith("192.168")]

try:
    nombre_de_threads = int(input("Nombre de threads : "))
except:
    nombre_de_threads = 10000
print("Lancement avec", nombre_de_threads, "threads.")

q = Queue()


def scan():
    global q
    while True:
        url = q.get()
        try:
            r = requests.get(url)
            r.raise_for_status()
        except:
            pass
        else:
            print("[+]", url)
        q.task_done()

def main():
    global q

    for adresse_ip in adresses_ip:
        q.put("http://" + adresse_ip)
    for i in range(256):
        for j in range(256):
            q.put("http://192.168." + str(i) + "." + str(j))
    
    for _ in range(nombre_de_threads):
        worker = Thread(target=scan)
        worker.daemon = True
        worker.start()


main()
q.join()

print("Fin.")
while 1:
    input()
