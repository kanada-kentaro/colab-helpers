from google.colab import drive
import subprocess
import sys
import importlib

def run_shell(cmd):
    res = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    sys.stdout.write(res.stdout)

def mount_drive(path):
    drive.mount(path)

def register_git_ssh_key(ssh_path, email, user_name):
    run_shell("rm -rf /root/.ssh/")
    run_shell("cp -r {} /root/.ssh || chmod 700 /root/.ssh".format(ssh_path))
    run_shell("ssh-keyscan github.com >> /root/.ssh/known_hosts")
    run_shell("chmod 644 /root/.ssh/known_hosts")
    run_shell("git config --global user.email {}".format(email))
    run_shell("git config --global user.name {}".format(user_name))


def git(repo_path, command):
    run_shell("git -C {} {}".format(repo_path, command))

def reload_from_str(modules, globals):
    if type(modules) == str:
        str_modules = [x.strip() for x in modules.split(',')]
        modules = [importlib.import_module(x) for x in str_modules]
    for module in modules:
        reload(module, globals)

def reload(module, globals):
    if type(module) == str:
        importlib.import_module(module)
        module = sys.module[module]
    importlib.reload(module)
    funcs = [func for func in dir(module) if not func.startswith('__')]
    for func_name in funcs:
        globals()[func_name] = module.__dict__[func_name]