import this

import requests as r
from threading import Thread
import os
import uuid
import time
import datetime

from itertools import cycle
import bot
import variables



with open("limiteds.txt", "r") as f:
    limiteds = f.read().replace(" ", "").split(",")

with open("cookie.txt", "r") as f:
    cookie = f.read()

with open("proxies.txt", "r") as f:#################
    proxies = f.read().splitlines()
    proxy_pool = cycle(proxies)
    proxy = next(proxy_pool)

user_id = r.get("https://users.roblox.com/v1/users/authenticated", cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy}).json()["id"]
x_token = ""
def get_x_token():
    global x_token

    x_token = r.post("https://auth.roblox.com/v2/logout",
                     cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy}).headers["x-csrf-token"]
    print("Logged in.")

    while 1:
        # Gets the x_token every 4 minutes.
        x_token = r.post("https://auth.roblox.com/v2/logout",
                         cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy}).headers["x-csrf-token"]
        time.sleep(248)


def buy(json, itemid, productid):
    print("Spam buying limited...")
    Thread(target=bot.StartCollect, args=(productid)).start()
    data = {
        "collectibleItemId": itemid,
        "expectedCurrency": 1,
        "expectedPrice": 0,
        "expectedPurchaserId": user_id,
        "expectedPurchaserType": "User",
        "expectedSellerId": json["creatorTargetId"],
        "expectedSellerType": "User",
        "idempotencyKey": "random uuid4 string that will be your key or smthn",
        "collectibleProductId": productid
    }

    while 1:
        data["idempotencyKey"] = str(uuid.uuid4())
        bought = r.post(f"https://apis.roblox.com/marketplace-sales/v1/item/{itemid}/purchase-item", json=data,
            headers={"x-csrf-token": x_token}, cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy})

        if bought.reason == "Too Many Requests":
            print("Ran into a ratelimit resuming trying again shortly...")
            proxy = next(proxy_pool)  # switch proxy
            time.sleep(0.5)
            continue

        try:
            bought = bought.json()
        except:
            print(bought.reason)
            print("Json decoder error whilst trying to buy item.")
            continue

        if not bought["purchased"]:
            print(f"Failed buying the limited, trying again.. Info: {bought} - {data}")
        else:
            ###################
            print(f"Successfully bought the limited! Info: {bought} - {data}")
            bot.DoneCollect(itemid)

        info = r.post("https://catalog.roblox.com/v1/catalog/items/details",
                      json={"items": [{"itemType": "Asset", "id": int(limited)}]},
                      headers={"x-csrf-token": x_token}, cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+prox})
        try:
            left = info.json()["data"][0]["unitsAvailableForConsumption"]
        except:
            print(f"Failed getting stock. Full log: {info.text} - {info.reason}")
            left = 0

        if left == 0:
            print("Couldn't buy the limited in time. Better luck next time.")
            bot.DoneCollectWithError(itemid)
            return


# Get collectible and product id for all the limiteds.
Thread(target=get_x_token).start()

print("UGC Sniper ---")
while x_token == "":
    time.sleep(0.01)

# https://apis.roblox.com/marketplace-items/v1/items/details
# https://catalog.roblox.com/v1/catalog/items/details

Thread(target=bot.START_BOT).start()
############variables.LIMITS = limiteds
cooldown = 60/(39/1)-0.9#60/(39/len(limiteds))-0.8


def CheckLimitedsFunc(limited, proxy):
    Skip = False
    print("Check limited - " + str(limited))
    try:
        info = r.post("https://catalog.roblox.com/v1/catalog/items/details",
                      json={"items": [{"itemType": "Asset", "id": int(limited)}]},
                      headers={"x-csrf-token": x_token}, cookies={".ROBLOSECURITY": cookie},
                      proxies={'http': "http://" + proxy}).json()["data"][0]
    except:  # except KeyError:
        print("Ratelimit! Waiting for next minute to start---")
        proxy = next(proxy_pool)
        print("New proxy - " + str(proxy))
        time.sleep(6.9)  # time.sleep((60-int(datetime.datetime.now().second)))
        Skip = True
        #continue

    if Skip != True and info.get("priceStatus", "") != "Off Sale" and info.get("collectibleItemId") is not None:
        productid = r.post("https://apis.roblox.com/marketplace-items/v1/items/details",
                           json={"itemIds": [info["collectibleItemId"]]},
                           headers={"x-csrf-token": x_token},
                           cookies={".ROBLOSECURITY": cookie}, proxies={'http':"http://"+proxy})

        try:
            productid = productid.json()[0]["collectibleProductId"]
        except:
            print(f"Something went wrong whilst getting the product id Logs - {productid.text} - {productid.reason}")
            Skip = True
            #continue

        if Skip != True:
            buy(info, info["collectibleItemId"], productid)


TryTimes = 0
while 1:
    if variables.PAUSE == False:
        start = time.perf_counter()

        for limited in variables.LIMITS:
            Thread(target=CheckLimitedsFunc, args=(limited, proxy)).start()

        taken = time.perf_counter()-start
        if taken < cooldown:
            time.sleep(cooldown-taken)

        os.system("cls")
        TryTimes+=1
        if TryTimes >= 4:
            TryTimes = 0
            proxy = next(proxy_pool)
            print("New proxy - " + str(proxy))

        print("Current proxy - " + str(proxy))
        print("Check done.\n"
              f"Time taken: {round(time.perf_counter()-start, 3)}\n"
              f"Ideal time: {round(cooldown, 3)}")
