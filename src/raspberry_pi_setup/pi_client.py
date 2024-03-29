from paramiko import SSHClient, AutoAddPolicy


class PiClient:
    def __init__(self, hostname, username="pi", password="raspberry"):
        self.ssh_client = SSHClient()
        self.ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        self.hostname = hostname
        self.username = username
        self.password = password

    def __enter__(self):
        self.ssh_client.connect(hostname=self.hostname, username=self.username, password=self.password)
        return self

    def __exit__(self, exit_type, value, traceback):
        self.ssh_client.close()

    def execute(self, command, input_lines=None):
        if input_lines is None:
            input_lines = []
        print(command)
        raw_stdin, raw_stdout, raw_stderr = self.ssh_client.exec_command(command)
        for line in input_lines:
            raw_stdin.write(f"{line}\n")
            raw_stdin.flush()
        stdout = raw_stdout.readlines()
        for line in stdout:
            print(line)

    def execute_ignore_stdout(self, command):
        print(command)
        self.ssh_client.exec_command(command)
