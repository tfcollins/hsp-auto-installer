import pyautogui as pag
import time
import os
import subprocess
from urllib import request
import signal

# Config
EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
download_folder = os.environ.get("DOWNLOAD_FOLDER") if os.environ.get("DOWNLOAD_FOLDER") else '/mlhsp/R2021b'
support_package = os.environ.get("SUPPORT_PACKAGE") if os.environ.get("SUPPORT_PACKAGE") else 'Communications Toolbox Support Package for X'

# Get downloader
url = "https://www.mathworks.com/supportfiles/downloads/R2022a/ssi_downloader/glnxa64/SupportSoftwareDownloader_R2022a_glnxa64.bin"
filename = "SupportSoftwareDownloader_R2022a_glnxa64.bin"
print("Downloading HSP downloader...")
request.urlretrieve(url, filename)
os.system(f"chmod +x {filename}")

# Launch
pid = subprocess.Popen(f"./{filename}")
print("Waiting for HSP downloader to launch...")
for i in range(1, 60):
    b = pag.locateOnScreen("center.png",confidence=0.7)
    print(i)
    time.sleep(1)
    if b:
        break
if not b:
    print("Not found")
    pid.poll()
    pid.send_signal(signal.SIGINT)
    exit(1)

if not os.path.exists("logs"):
    os.mkdir("logs")

print("Logging in...")
pag.screenshot('logs/login1.png')
x, y = pag.locateCenterOnScreen("center.png",confidence=0.7)
print(x,y)
pag.moveTo(x, y, duration=1)
pag.click()
time.sleep(1)
pag.typewrite(EMAIL, interval=0.1)
pag.press('tab')
pag.press('tab')
pag.press('tab')
pag.press('enter')

time.sleep(1)
pag.screenshot('logs/login2.png')
pag.typewrite(PASSWORD, interval=0.1)
time.sleep(1)
pag.press('enter')

print("Selecting ML versions...")
time.sleep(1)
pag.screenshot('logs/ml_version.png')
pag.press('tab')
pag.press('tab')
pag.press('space')
time.sleep(1)
x, y = pag.locateCenterOnScreen("next.png",confidence=0.7)
pag.click(x=x, y=y)

time.sleep(10)
print("Done Sleeping, selecting Support Package...")
pag.press('tab')
pag.press('tab')
pag.press('tab')
# x, y = pag.locateCenterOnScreen("filter_list.png",confidence=0.7)
# pag.click(x=x, y=y)

pag.typewrite(support_package, interval=0.1)
time.sleep(1)
x, y = pag.locateCenterOnScreen("check_box.png",confidence=0.7)
pag.click(x=x, y=y)
time.sleep(1)
x, y = pag.locateCenterOnScreen("next.png",confidence=0.7)
pag.screenshot('logs/pick_hsp.png')
pag.click(x=x, y=y)

time.sleep(4)
print("Changing download location...")
pag.press('tab')
pag.press('tab')
pag.press('tab')
pag.press('tab')
pag.press('tab')
pag.typewrite(download_folder, interval=0.1)
pag.press('tab')
pag.press('tab')
pag.screenshot('logs/change_dl_location.png')
pag.press('enter')

time.sleep(1)
print("Agreeing to terms...")
pag.press('tab')
pag.screenshot('logs/terms.png')
pag.press('enter')

time.sleep(5)
print("Start download...")
pag.press('tab')
pag.screenshot('logs/start_dl.png')
pag.press('enter')

# Wait for download
print("Waiting for HSP download...")
pag.screenshot('logs/waiting.png')
for i in range(1, 60*10):
    b = pag.locateOnScreen("close.png",confidence=0.95)
    print(i)
    time.sleep(1)
    if b:
        x, y = pag.locateCenterOnScreen("close.png",confidence=0.95)
        pag.click(x=x, y=y)
        break
if not b:
    pag.screenshot('logs/fail_dl.png')
    print("Download did not finish")
    pid.poll()
    pid.send_signal(signal.SIGINT)
    exit(1)
print("Download finished")
pag.screenshot('logs/done.png')
pid.send_signal(signal.SIGINT)
