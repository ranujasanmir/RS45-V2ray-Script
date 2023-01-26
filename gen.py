import json
import requests


config_list = []

for port in range(23, 65536):
    sample = {
        "port": port,
        "protocol": "vless",
        "settings": {
            "clients": [
                {
                    "id": "9b273998-cf4c-4457-b596-3746e3f9fd3a"
                }
            ],
            "decryption": "none"
        },
        "streamSettings": {
            "network": "ws",
            "security": "tls",
            "tlsSettings": {
                "certificates": [
                    {
                        "certificateFile": "/etc/xray/xray.crt",
                        "keyFile": "/etc/xray/xray.key"
                    }
                ]
            }
        }
    }
    config_list.append(sample)


with open("configs.json", "w") as outfile:
    json.dump(config_list, outfile)


# with open('configs.json') as json_file:
#     json_file = json.load(json_file)


# print(type(json_file))
