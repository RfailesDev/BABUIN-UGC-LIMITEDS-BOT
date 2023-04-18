import requests

def GetAssetImage(ID):
    print("----------")
    s = requests.session()
    ret = s.post("https://thumbnails.roblox.com/v1/batch", json=[{"requestId": str(ID)+"::Asset:420x420:png:regular", "type": "Asset", "targetId": str(ID), "token": "", "format": "png", "size": "420x420"}])
    p = ret.text.split("imageUrl")[1].split("}")[0]
    print(ret.text)
    print(p)
    url = p[3:-1]
    print("--")
    print(url)
    print("----------")
    return url