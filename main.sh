apt update
apt upgrade -y
apt -y install python3.10 python3.10-venv python3-pip
bash v2ray.sh
pip3 install -r requirements.txt
mkdir /root/bot
cp bot.py /root/bot
cp bot.sh /root/bot
chmod +x /root/bot/bot.sh
cp horapusa.service /etc/systemd/system/
sudo systemctl enable rs45.service
sudo systemctl start rs45.service
