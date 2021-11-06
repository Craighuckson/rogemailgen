import subprocess

cd = "C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\"

rc = subprocess.run(
    "C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\connect.bat",
    cwd=cd,
    capture_output=True,
    text=True,
)

print('Making VPN connection...')
if rc.returncode == 0:
    print("VPN connected")
else:
    print("There was a problem")
