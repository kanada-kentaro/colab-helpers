from google.colab import drive

def mount_drive(path):
    drive.mount(path)

def register_git_ssh_key(ssh_path, email, user_name):
    ! rm - rf / root /.ssh /
    ! cp -r {ssh_path} /root/.ssh || chmod 700 /root/.ssh
    ! ssh-keyscan github.com >> /root/.ssh/known_hosts
    ! chmod 644 /root/.ssh/known_hosts
    ! git config --global user.email {email}
    ! git config --global user.name {user_namee}

