import itertools
import string
import requests
import threading
import time
import queue

start = time.time()
q = queue.Queue()


def color(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


availablePlates = []


def checkLicencePlate():
    while True:
        plate = q.get()
        url = (
            "https://www.myplates.com/api/licenseplates/passenger/small-star-black/"
            + str(plate)
        )
        res = requests.get(url).json()
        if res["status"] == "not-available":
            print(color(245, 69, 66, "Not Available : " + plate))
        if res["status"] == "available":
            print(color(0, 255, 25, "Available : " + plate))
            availablePlates.append(plate)
        q.task_done()


def convertTuple(tup):
    str = ""

    for item in tup:
        str = str + item
    return str


letters1 = list(string.ascii_lowercase)
letters2 = list(string.ascii_lowercase)
iterables = letters1, letters2

threads = []

for plate in itertools.product(*iterables):
    plate = convertTuple(plate)
    q.put(plate)

for item in range(20):
    t = threading.Thread(target=checkLicencePlate, daemon=True).start()
    threads.append(t)


q.join()

end = time.time()
secconds = end - start
minutes = secconds / 60
print(color(0, 255, 255, str(secconds) + " secconds"))
print(color(0, 255, 255, str(minutes) + " minutes"))

print(color(0, 255, 255, "--------------------------------"))
print(color(0, 255, 255, availablePlates))
