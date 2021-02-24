from raspberry_pi_setup.config import PI_IP_ADDRESS, PI_ROOT_PASSWORD
from raspberry_pi_setup.pi_client import PiClient


def general_preparation():
    with PiClient(PI_IP_ADDRESS) as pi:
        # general setup
        pi.execute("sudo apt -y update")
        pi.execute("sudo apt -y upgrade")
        pi.execute("sudo apt -y install cmake git")

        # only necessary for remote development
        pi.execute("sudo passwd root", input_lines=[PI_ROOT_PASSWORD, PI_ROOT_PASSWORD])
        pi.execute("echo 'PermitRootLogin yes' | sudo tee -a /etc/ssh/sshd_config")
        pi.execute_ignore_stdout("sudo service sshd restart")


def install_zmq():
    with PiClient(PI_IP_ADDRESS) as pi:
        pi.execute("sudo apt -y install libzmq3-dev")
        pi.execute("git clone https://github.com/zeromq/cppzmq.git")
        pi.execute("cd cppzmq && git checkout v4.7.1")
        pi.execute("cd cppzmq && mkdir build")
        pi.execute("cd cppzmq/build && cmake -DCPPZMQ_BUILD_TESTS=OFF ..")
        pi.execute("cd cppzmq/build && sudo make -j4 install")


def install_spdlog():
    with PiClient(PI_IP_ADDRESS) as pi:
        pi.execute("sudo apt -y install libspdlog-dev")
