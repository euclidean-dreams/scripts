from raspberry_pi_setup.pi_client import PiClient


def general_preparation(config):
    with PiClient(config.pi_ip_address) as pi:
        # general setup
        pi.execute("sudo apt -y update")
        pi.execute("sudo apt -y upgrade")
        pi.execute("sudo apt -y install cmake git")
        pi.execute(f"git config --global user.email \"{config.git_email}\"")
        pi.execute(f"git config --global user.name \"{config.git_username}\"")

        # only necessary for remote development
        pi.execute("sudo passwd root", input_lines=[config.pi_root_password, config.pi_root_password])
        pi.execute("echo 'PermitRootLogin yes' | sudo tee -a /etc/ssh/sshd_config")
        pi.execute_ignore_stdout("sudo service sshd restart")

    with PiClient(config.pi_ip_address, username="root", password=config.pi_root_password) as pi:
        pi.upload_file(config.ssh_key_path, "/root/.ssh/id_rsa")
        pi.upload_file(f"{config.ssh_key_path}.pub", "/root/.ssh/id_rsa.pub")
        pi.execute("chmod 600 /root/.ssh/id_rsa")
        pi.execute("chmod 600 /root/.ssh/id_rsa.pub")
        pi.execute("ssh-keyscan -H github.com >> ~/.ssh/known_hosts")


def install_zmq(config):
    with PiClient(config.pi_ip_address) as pi:
        pi.execute("sudo apt -y install libzmq3-dev")
        pi.execute("git clone https://github.com/zeromq/cppzmq.git")
        pi.execute("cd cppzmq && git checkout v4.7.1")
        pi.execute("cd cppzmq && mkdir build")
        pi.execute("cd cppzmq/build && cmake -DCPPZMQ_BUILD_TESTS=OFF ..")
        pi.execute("cd cppzmq/build && sudo make -j4 install")


def install_spdlog(config):
    with PiClient(config.pi_ip_address) as pi:
        pi.execute("sudo apt -y install libspdlog-dev")
