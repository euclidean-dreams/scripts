from raspberry_pi_setup.config import load_config, YAML_PATH


def main():
    config = load_config(YAML_PATH)
    wpa_supplicant_body = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country={config.network_country_code}
    
    network={{
        ssid="{config.network_ssid}"
        psk="{config.network_password}"
    }}
    """

    with open(f"{config.boot_directory_path}/wpa_supplicant.conf", mode="w+") as wpa_supplicant_file:
        wpa_supplicant_file.write(wpa_supplicant_body)

    with open(f"{config.boot_directory_path}/ssh", mode="w+") as ssh_file:
        ssh_file.write("")


if __name__ == "__main__":
    main()
