# type: ignore pylance drunk
import paramiko
import getpass
import os

# Clear the terminal screen
def clear():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:
        os.system('clear') # For Linux and macOS


# Fill in this data
path_to_repo = '' # folder containing both frontend and backend
frontend_folder = '' # react folder
backend_folder= '' # django folder
host = ''
port = ''
username = ''
password = getpass.getpass('Password:')

# Terminal command to execute
yarn_build = 'yarn run build'
run_migrations = f'python manage.py migrate && echo {password} | sudo -S supervisorctl restart all'
checkout = 'git checkout'
fetch = 'git fetch'
pull = 'git pull'

# Create SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Menu
print("What do you wanna update?")
print("1 - update everything")
print("2 - update backend")
print("3 - update frontend")
update_mode = input()
clear()

print("Pick an enviroment to update:")
print("1 - dev")
print("2 - testing")
env = input()
clear()

env = "dev" if env == "1" else "tst"

# Directories
cd_backend = f'cd {path_to_repo}/{env}/{backend_folder}'
cd_frontend = f'cd {path_to_repo}/{env}/{frontend_folder}'
activate_venv = f'source {path_to_repo}/{env}/{backend_folder}/env/bin/activate'

backend_target_branch = ""
frontend_target_branch = ""

# Prompt user for branch names
if env == "tst":
    if update_mode == "1" or update_mode == "2":
        backend_target_branch = input("Enter the backend's target branch name: ")
    if update_mode == "1" or update_mode == "3":
        frontend_target_branch = input("Enter the frontend's target branch name: ")

    git_update_backend = f'''
        {fetch} &&
        {checkout} {backend_target_branch}
    '''
    git_update_frontend = f'''
        {fetch} &&
        {checkout} {frontend_target_branch}
    '''

elif env == "dev":
    git_update_backend = f'{fetch} && {pull}'
    git_update_frontend = f'{fetch} && {pull}'


# Builds
deploy_migrations = f'''
        {cd_backend} && 
        {git_update_backend} && 
        {activate_venv} && 
        {run_migrations}
    '''

deploy_react_build = f'''
        {cd_frontend} && 
        {git_update_frontend} && 
        {yarn_build}
    '''

try:
    # Connect to the SSH server
    ssh_client.connect(host, port, username, password)
    print("Connected to the server")

    if update_mode == "1" or update_mode == "2":
        stdin, stdout, stderr = ssh_client.exec_command(deploy_migrations)
        output = stdout.read().decode()
        print(output)

        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            print("Migration compleated.")
            print(stdout.read().decode())
        else:
            print("Migration execution failed.")
            print(stderr.read().decode())

    if update_mode == "1" or update_mode == "3":
        stdin, stdout, stderr = ssh_client.exec_command(deploy_react_build)
        output = stdout.read().decode()
        print(output)

        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            print("Builded correctly.")
            print(stdout.read().decode())
        else:
            print("Build failed.")
            print(stderr.read().decode())

finally:
    ssh_client.close()
