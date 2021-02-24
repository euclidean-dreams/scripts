from raspberry_pi_setup.prepare.shared import general_preparation, install_zmq, install_spdlog


def main():
    general_preparation()
    install_zmq()
    install_spdlog()


if __name__ == "__main__":
    main()
