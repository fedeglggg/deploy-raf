# type: ignore pylance drunk
import paramiko
import getpass
import os

# Clear the terminal screen
def clear_terminal():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For Linux and macOS
        os.system('clear')

# SSH server details (add yours)
host = ''
port = 
username = ''
password = getpass.getpass('Password:')

# Menu
print("What do you wanna update?")
print("1 - update everything")
print("2 - only backend")
print("3 - only frontend")
picked_input = input()

if picked_input == "1":
    update_backend = True
    update_frontend = True
if picked_input == "2":
    update_backend = True
    update_frontend = False
if picked_input == "3":
    update_backend = False
    update_frontend = True

clear_terminal()

print("Pick an enviroment to update:")
print("1 - dev (developing)")
print("2 - tst (testing)")
picked_input = input()

if picked_input == "1":
    enviroment = "dev"
if picked_input == "2":
    enviroment = "tst"

clear_terminal()

if enviroment == "tst":
    if update_backend:
        backend_target_branch = input("Enter the backend's target branch name: ")
    if update_frontend:
        frontend_target_branch = input("Enter the frontend's target branch name: ")

    git_update_backend = f'{fetch} && {checkout} {backend_target_branch}'
    git_update_frontend = f'{fetch} && {checkout} {frontend_target_branch}'

elif enviroment == "dev":
    git_update_backend = f'{fetch} && {checkout} dev && {pull}'
    git_update_frontend = f'{fetch} && {checkout} dev && {pull}'

# Directories (add yours)
project_directory = ""
backend_directory = ""
frontend_directory = ""

cd_backend = f'cd {project_directory}/{enviroment}/{backend_folder}'
cd_frontend = f'cd {project_directory}/{enviroment}/{frontend_directory}'

# Terminal command to execute
yarn_build = 'yarn run build'
activate_venv = f'source {project_directory}/{enviroment}/{backend_folder}/env/bin/activate'
run_migrations = f'python manage.py migrate && echo {password} | sudo -S supervisorctl restart all'
checkout = 'git checkout'
fetch = 'git fetch'
pull = 'git pull'

# Create SSH client
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Builds
deploy_migrations = f'{cd_backend} && {git_update_backend} && {activate_venv} && {run_migrations}'
deploy_react_build = f'{cd_frontend} && {git_update_frontend} && {yarn_build}'

try:
    # Connect to the SSH server
    ssh_client.connect(host, port, username, password)
    print("Connected to the server")

    if update_backend:
        print("Running ", deploy_migrations)
        stdin, stdout, stderr = ssh_client.exec_command(deploy_migrations)
        output = stdout.read().decode()
        print(output)

        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            print("Migration compleated.")
        else:
            print("Migration execution failed.")
        
        print(stderr.read().decode())

    if update_frontend:
        print("Running ", deploy_react_build)
        stdin, stdout, stderr = ssh_client.exec_command(deploy_react_build)
        output = stdout.read().decode()
        print(output)

        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            print("Builded correctly.")
        else:
            print("Build failed.")

        print(stderr.read().decode())

finally:
    ssh_client.close()
