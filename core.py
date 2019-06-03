import subprocess
import sys
from google.colab import drive, auth
# import tensorflow as tf
import pprint
import json


def run_shell(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    sys.stdout.write(res.stdout)
    sys.stdout.write(res.stderr)
    return res


def git(repo_path, command):
    run_shell("git -C {} {}".format(repo_path, command))


def mount_drive(path):
    drive.mount(path)


def register_gcp():
    auth.authenticate_user()


def setup_tpu(ex_globals):
    for key, value in ex_globals.items():
        if not key.startswith('__'):
            globals()[key] = value
    tpu_addr = os.environ.get('COLAB_TPU_ADDR')
    if tpu_addr:
        ex_globals['TPU_ADDRESS'] = 'grpc://' + tpu_addr
        with tf.Session(ex_globals['TPU_ADDRESS']) as session:
            print('TPU devices:')
            pprint.pprint(session.list_devices())

            # Upload credentials to TPU.
            with open('/content/adc.json', 'r') as f:
                auth_info = json.load(f)
            tf.contrib.cloud.configure_gcs(session, credentials=auth_info)


def register_git_ssh_key(ssh_path, email, user_name):
    run_shell("rm -rf /root/.ssh/")
    run_shell("cp -r {} /root/.ssh".format(ssh_path))
    run_shell("chmod 700 /root/.ssh")
    run_shell("ssh-keyscan github.com >> /root/.ssh/known_hosts")
    run_shell("chmod 644 /root/.ssh/known_hosts")
    run_shell("git config --global user.email {}".format(email))
    run_shell("git config --global user.name {}".format(user_name))
