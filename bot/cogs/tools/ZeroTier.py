import datetime
import requests
import os


def get_network_users():
    headers = {
        'Authorization': f'token {os.environ["ZT_TOKEN"]}',
        'Content-Type': 'application/json',
    }
    data = requests.get(f"https://api.zerotier.com/api/v1/network/{os.environ['ZT_NETWORK']}/member",
                        headers=headers).json()
    result_dict = {}
    for member in data:
        delta = datetime.datetime.fromtimestamp(member["clock"] / 1000) \
                - datetime.datetime.fromtimestamp(member["lastSeen"] / 1000)
        if delta < datetime.timedelta(minutes=1):
            message = "Less than a minute ago"
        else:
            if delta < datetime.timedelta(hours=1):
                delta = round(delta.total_seconds() / 60)
                unit = "minute"
            elif delta < datetime.timedelta(days=1):
                delta = round(delta.total_seconds() / 3600)
                unit = "hour"
            elif delta < datetime.timedelta(days=30):
                delta = delta.days
                unit = "day"
            else:
                delta = round(delta.days / 30)
                unit = "month"

            text = unit if delta == 1 else unit + "s"
            message = f"About {delta} {text} ago."
        result_dict.update({member["name"].ljust(25): message})
    return result_dict
