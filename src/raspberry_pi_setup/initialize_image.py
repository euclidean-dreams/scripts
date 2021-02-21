from raspberry_pi_setup.config import NETWORK_COUNTRY_CODE, NETWORK_SSID, NETWORK_PASSWORD, BOOT_DIRECTORY_PATH


def main():
    wpa_supplicant_body = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country={NETWORK_COUNTRY_CODE}
    
    network={{
        ssid="{NETWORK_SSID}"
        psk="{NETWORK_PASSWORD}"
    }}
    """

    with open(f"{BOOT_DIRECTORY_PATH}/wpa_supplicant.conf", mode="w+") as wpa_supplicant_file:
        wpa_supplicant_file.write(wpa_supplicant_body)

    with open(f"{BOOT_DIRECTORY_PATH}/ssh", mode="w+") as ssh_file:
        ssh_file.write("")


if __name__ == "__main__":
    main()
