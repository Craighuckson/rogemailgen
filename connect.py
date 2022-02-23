import subprocess
import PySimpleGUI as sg
import os
sg.theme('Dark Blue 8')

layout = [[sg.Text('Waiting for VPN')],
         [sg.Text(key='-OUT-')]]
window = sg.Window('VPN CONNECTING',layout)

#cd = "C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\"

#os.system('net stop vpnagent')
#os.system('net start vpnagent')
os.chdir('C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\')
os.system('connect.bat')
print('Connected')
'''
rc = subprocess.Popen(
     "C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\connect.bat")
while True:
    if rc.poll() is not None:
        break
    event, value = window.read()
    window.refresh()
print("VPN connected")
'''