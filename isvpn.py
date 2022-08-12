import subprocess

def is_vpn():
	vpn_out = subprocess.run(r'"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpncli.exe" "status"', capture_output=True,text=True)
	#print(vpn_out)
	if "Connected" in vpn_out.stdout:
		return True
	else:
		return False


if __name__ == '__main__':
	with open('C:\\Users\\Cr\\vpnstatus.txt','w') as v:
		v.write(str(is_vpn()))