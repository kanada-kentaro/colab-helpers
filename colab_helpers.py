from google.colab import drive
import subprocess
import sys

def run_shell(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE)
    sys.stdout.write(res.stdout)

def mount_drive(path):
    drive.mount(path)

def register_git_ssh_key(ssh_path, email, user_name):
    run_shell("rm - rf / root /.ssh /")
    run_shell("cp -r {} /root/.ssh || chmod 700 /root/.ssh".format(ssh_path))
    run_shell("ssh-keyscan github.com >> /root/.ssh/known_hosts")
    run_shell("chmod 644 /root/.ssh/known_hosts")
    run_shell("git config --global user.email {}".format(email))
    run_shell("git config --global user.name {}".format(user_name))