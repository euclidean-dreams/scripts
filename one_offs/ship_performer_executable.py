from pi_client import PiClient
from raspberry_pi_setup.config import load_config, YAML_PATH

config = load_config(YAML_PATH)
with PiClient(config.pi_ip_address) as pi:
    pi.execute("sudo sshpass -p raspberry scp /root/performer-deployment/cmake-build-release-conductor/performer "
               "pi@10.0.0.220:/home/pi/performer")
