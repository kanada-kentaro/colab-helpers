from google.colab import drive
import subprocess
import sys
import importlib
import tensorflow as tf
import os
import msgpack
import msgpack_numpy as m

def run_shell(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    sys.stdout.write(res.stdout)
    sys.stdout.write(res.stderr)
    return res

def mount_drive(path):
    drive.mount(path)

def register_git_ssh_key(ssh_path, email, user_name):
    run_shell("rm -rf /root/.ssh/")
    run_shell("cp -r {} /root/.ssh".format(ssh_path))
    run_shell("chmod 700 /root/.ssh")
    run_shell("ssh-keyscan github.com >> /root/.ssh/known_hosts")
    run_shell("chmod 644 /root/.ssh/known_hosts")
    run_shell("git config --global user.email {}".format(email))
    run_shell("git config --global user.name {}".format(user_name))


def git(repo_path, command):
    run_shell("git -C {} {}".format(repo_path, command))

# reload modules
def reloads(modules, globals):
    if type(modules) == str:
        modules = [x.strip() for x in modules.split(',')]
    for module in modules:
        reload(module, globals)

def reload(module, globals):
    if type(module) == str:
        importlib.import_module(module)
        module = sys.modules[module]
    importlib.reload(module)
    funcs = [func for func in dir(module) if not func.startswith('__')]
    for func_name in funcs:
        globals[func_name] = module.__dict__[func_name]

# save/load from buckets
def is_exist_in_bucket(*fnames):
    fname = os.path.join(*fnames)
    res = run_shell("gsutil -q stat {}".format(fname))
    return res.returncode == 0

def save_to_bucket(bucket_directory, fname):
  tf.gfile.MakeDirs(bucket_directory)
  bucket_fname = os.path.join(bucket_directory, fname)
  run_shell("gsutil cp {} {}".format(fname, bucket_fname))

def load_from_bucket(bucket_directory, fname):
  bucket_fname = os.path.join(bucket_directory, fname)
  run_shell("gsutil cp {} {}".format(bucket_fname,fname))

def pop_arg(kwargs, arg):
    if arg in kwargs:
        value = kwargs[arg]
        del kwargs[arg]
        return value
    else:
        return None

def load_or_execute(bucket_directory, fname, func, *args, **kwargs):
    force_execution = pop_arg(kwargs, "force_execution")
    load = pop_arg(kwargs, "load")
    if force_execution or not is_exist_in_bucket(bucket_directory, fname):
        print("file {} doesn't exist in {}. execute function...".format(fname, bucket_directory))
        func(*args, **kwargs)
        save_to_bucket(bucket_directory, fname)
    else:
        if load:
            print("file {} exist in {}. load file...".format(fname, bucket_directory))
            load_from_bucket(bucket_directory, fname)

def bucket_dir(bucket_name, *dir_names):
    bucket_name = 'gs://{}'.format(bucket_name)
    dir_name =  os.path.join(*dir_names)
    return os.path.join(bucket_name, dir_name)

def to_mpack(data, fname):
    packer = msgpack.Packer(default=m.encode)
    with open(fname, "wb") as file:
        file.write(packer.pack(data))

def load_mpack(fname):
    return msgpack.unpack(open(fname, "rb"), object_hook=m.decode)

def mpack_loader(fname):
    return msgpack.Unpacker(open(fname, "rb"), object_hook=m.decode)