import platform
from termcolor import colored
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import psutil
from config import *


def unit(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def clr(text):
    colorgrn = colored(f"{text}", "green")
    return colorgrn


def monitor():
    uname = platform.uname()
    cpufreq = psutil.cpu_freq()
    mem = psutil.virtual_memory()
    internet = psutil.net_io_counters()
    sys = uname.system
    core = psutil.cpu_count(logical=True)
    cpu_freq_mx = cpufreq.max
    mem_total = (int(mem.total)) / (1024 * 1024 * 1024)

    output = f"""
    {"=" * 20} SYSTEM Info {"=" * 20}
            <b>System</b>       - {sys}
            <b>Total Cores</b>  - {core} Cores
            <b>Cpu Usage</b>    - {psutil.cpu_percent()}%
            <b>Max Cpu Freq</b> - {cpu_freq_mx}MHZ
            <b>Total Ram</b>    - {round(mem_total)}GB
            <b>Ram in Use</b>   - {unit(mem.used)} | {mem.percent}%
    {"=" * 20} Internet {"=" * 24}        
            <b>Data Sent</b>    - {unit(internet.bytes_sent)}
            <b>Data Receive</b> - {unit(internet.bytes_recv)}
            
            <b>Copyright © 2023 RS45 V2RAY SCRIPT</b>

    """
    return output


###############################################################################################

sudo = 1436625686

r = requests.get('https://ip4.seeip.org')
IP_address = r.text

# with open("/root/bot/bot.token", "r") as token:
#     bot_token = token.read()
#     bot_token = str(bot_token)

bot_token = "5898254126:AAHYlGymgf8O8D4i_VQptt8FFscTqoMWSfk"
updater = Updater(bot_token, use_context=True, parse_mode= "html")


def start(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text("""<b>Hello dear! Welcome to the RS45 Server Management Bot.</b>
    Please write
    /help to see the commands available.
    
    <b>This script is developed by Ranuja Sanmira</b>""")


def help(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text("""<b>Available Commands</b> :-
        /speed_test - test server speed.
        /hardware_usage - check hardware usage.
        /vless - create v2ray vless config.
        /v2ray_all_configs - show all v2ray configs.
        /reboot_server - reboot the server.""")


def vless(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        port = update.message.text[7:]
        try:
            vless_config = vless_ws_gen(port)
            update.message.reply_text(vless_config)
        except Exception:
            update.message.reply_text("Faild to create vless config.")


def vmess(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        port = update.message.text[7:]
        try:
            vmess_config = vless_ws_gen(port)
            update.message.reply_text(vmess_config)
        except Exception:
            update.message.reply_text("Faild to create vmess config.")


def speed_test(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            import speedtest

            # If you want to test against a specific server
            # servers = [1234]

            threads = None
            # If you want to use a single threaded test
            # threads = 1

            s = speedtest.Speedtest()
            s.get_best_server()
            s.download(threads=threads)
            s.upload(threads=threads)
            s.results.share()

            results_dict = s.results.dict()
            print(results_dict["share"])
            update.message.chat.send_photo(results_dict["share"])

        except Exception:
            update.message.reply_text("speedtest faild.")


def unknown(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text(
            "Sorry '%s' is not a valid command" % update.message.text)


def reboot_server(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            update.message.reply_text("Rebooting...")
            os.system("reboot")
        except Exception:
            update.message.reply_text("Reboot faild.")


def hardware_usage(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        try:
            sys_usage = monitor()
            update.message.reply_text(sys_usage)
        except Exception:
            update.message.reply_photo("faild to get hardware info.")


def unknown_text(update: Update, context: CallbackContext):
    if update.message.chat.id == sudo:
        update.message.reply_text(
            "Sorry I can't recognize you , you said '%s'" % update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('vless', vless))
# updater.dispatcher.add_handler(CommandHandler('v2ray_all_configs', v2ray_all_configs))
updater.dispatcher.add_handler(CommandHandler('speed_test', speed_test))
updater.dispatcher.add_handler(CommandHandler('hardware_usage', hardware_usage))
updater.dispatcher.add_handler(CommandHandler('reboot_server', reboot_server))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands

# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
