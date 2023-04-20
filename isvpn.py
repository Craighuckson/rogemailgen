import subprocess

VPNPATH = (
    '"C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\vpncli.exe" "status"'
)


def is_vpn():
    """Check if VPN is connected"""
    vpn_out = subprocess.run(
            VPNPATH,
            capture_output=True, text=True)
    # print(vpn_out)
    if "Connected" in vpn_out.stdout:
        return True
    else:
        return False


if __name__ == '__main__':
    with open('C:\\Users\\Cr\\vpnstatus.txt', 'w') as v:
        v.write(str(is_vpn()))
