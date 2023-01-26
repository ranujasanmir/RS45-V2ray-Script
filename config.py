import os

import requests
import json

public_ip = requests.get('https://api.ipify.org')
public_ip = public_ip.text

sample_vless_ws_config = {
    "port": 443,
    "protocol": "vless",
    "settings": {
        "clients": [
            {
                "id": "$UUID"
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


def vless_ws_gen(port):
    with open('/usr/local/etc/xray/config.json') as json_file:
        json_file = json.load(json_file)
    with open('configs.json') as json_all_configs_file:
        json_all_configs_file = json.load(json_all_configs_file)
    json_file["inbounds"] = json_all_configs_file
    vless_config = f"""vless://"9b273998-cf4c-4457-b596-3746e3f9fd3a"@{public_ip}:{port}?security=tls&encryption=none&type=ws&sni=hora.pusa.vpn#Hora-Pusa-VPN"""
    with open('/usr/local/etc/xray/config.json', 'w') as json_write:
        json.dump(json_file, json_write)
    os.system("sudo service xray restart")
    return vless_config

