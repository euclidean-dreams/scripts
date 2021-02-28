import yaml

YAML_PATH = "secrets/config.yml"


class Config(yaml.YAMLObject):
    yaml_tag = "!config"

    def __init__(self,
                 boot_directory_path,
                 network_country_code,
                 network_ssid,
                 network_password,
                 pi_ip_address,
                 pi_root_password,
                 ssh_key_path):
        self.boot_directory_path = boot_directory_path
        self.network_country_code = network_country_code
        self.network_ssid = network_ssid
        self.network_password = network_password
        self.pi_ip_address = pi_ip_address
        self.pi_root_password = pi_root_password
        self.ssh_key = ssh_key_path


def load_config(file_path):
    yaml.add_path_resolver("!config", ["Config"], dict)
    try:
        with open(file_path, "r") as config_file:
            data = yaml.full_load(config_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"please create a config file at {YAML_PATH} using the provided template "
                                f"and ensure your working directory is the repo root")
    config = data.get("Config", None)
    if config is not None:
        return config
    else:
        raise ValueError(f"could not find Config object in yaml at: {file_path}")
