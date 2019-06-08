import subprocess
import sys
from google.colab import drive, auth
import tensorflow as tf
import os
import pprint
import json
from importlib.util import spec_from_file_location,module_from_spec
import pathlib


def run_shell(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    sys.stdout.write(res.stdout)
    sys.stdout.write(res.stderr)
    return res


def git(repo_path, command):
    run_shell("git -C {} {}".format(repo_path, command))


def git_pull(repo_path, branch_name):
    git(repo_path, "fetch")
    git(repo_path, "reset --hard origin/{}".format(branch_name))


def mount_drive(path):
    drive.mount(path)


def register_gcp():
    auth.authenticate_user()


def setup_tpu(ex_globals):
    """
    setup gpu

    Args:
        ex_globals (dict): globals() called in notebook
    """
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
    """
    register ssh-key with colab VM in order to access private repository,
    Uploading ssh-key may cause security problems. Please use at your own risk.

    Args:
        ssh_path (str): the path of the directory that contains ssh key
        email (str): git email
        user_name (str): git username
    """
    run_shell("rm -rf /root/.ssh/")
    run_shell("cp -r {} /root/.ssh".format(ssh_path))
    run_shell("chmod 700 /root/.ssh")
    run_shell("ssh-keyscan github.com >> /root/.ssh/known_hosts")
    run_shell("chmod 644 /root/.ssh/known_hosts")
    run_shell("git config --global user.email {}".format(email))
    run_shell("git config --global user.name {}".format(user_name))


def import_from_path(path, globals):
    path = pathlib.Path(path)
    if path.is_dir():
        files = [file for file in path.glob("**/[!__]*.py")  if not 'vendor' in str(file)]
        for file in files:
            __import_from_path(file, globals)
    else:
        __import_from_path(path, globals)


def __import_from_path(path, globals):
    module_name = path.stem
    spec = spec_from_file_location(module_name, str(path))
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    globals[module_name] = module
    funcs = [func for func in module.__dir__() if not func.startswith('__')]
    for func_name in funcs:
        globals[func_name] = module.__dict__[func_name]
