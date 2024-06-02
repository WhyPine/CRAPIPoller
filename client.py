import requests
from requests import delete as DEL
from requests import put as PUT
from requests import get as GET
from requests import post as POST
from uuid import uuid1
import json
import datetime


class CrunchyrollClient():
    def __init__(self, email, password) -> None:
        self.session = requests.session()
        self.endpoint = "https://beta-api.crunchyroll.com"
        self.email = email
        self.password = password
        self.auth_token = None
        self.refresh_token = None
        self.basic = "bm9haWhkZXZtXzZpeWcwYThsMHE6"
        self.account_id = None
        self.profile_id = None
        self.country = None
        self.expires_in = None
        self.expires_tstamp = None

    def auth(self):
        DEVICE_NAME = "Crunchyroll"
        DEVICE_TYPE = "Chrome on Android Auto"
        DEVICE_ID = str(uuid1())
        headers = {
            "Authorization" : "Basic {}".format(self.basic),
            "Etp-Anonymous-Id":"8a64f481-55ca-4757-9507-c07db5461386"
        }
        target="/auth/v1/token"
        payload={
            "username": self.email,
            "password": self.password,
            "grant_type":"etp_rt_cookie",
            "scope": "offline_access",
            "device_id": DEVICE_ID,
            "device_name": DEVICE_NAME,
            "device_type": DEVICE_TYPE
        }
        cookies = {"etp_rt": "e9f030ab-0fde-4778-a26b-1a2b8327bca1"}#e9f030ab-0fde-4778-a26b-1a2b8327bca1
        response = self.session.post((self.endpoint+target), headers=headers, data=payload, cookies=cookies)
        data = json.loads(response.text)
        self.session.cookies = response.cookies
        #print(data)
        self.access_token = data.get("access_token")
        self.refresh_token = data.get("refresh_token")
        self.account_id = data.get("account_id")
        self.profile_id = data.get("profile_id")
        self.country = data.get("country")
        self.expires_in = data.get("expires_in")
        if self.expires_in:
            self.expires_tstamp = datetime.date.today() + datetime.timedelta(seconds=self.expires_in)
        