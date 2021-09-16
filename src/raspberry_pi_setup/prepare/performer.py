from raspberry_pi_setup.config import load_config, YAML_PATH
from raspberry_pi_setup.prepare.shared import general_preparation, install_zmq, install_spdlog


def main():
    config = load_config(YAML_PATH)
    general_preparation(config)
    install_zmq(config)
    install_spdlog(config)


if __name__ == "__main__":
    main()
