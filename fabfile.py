from fabric.api import *
import os 

env.hosts = [os.environ["staging_url"]]
env.user = "ec2-user"
env.colorize_errors = True
env.key_filename = "./aws-keys.pem"

@task
def generate_new_keys():
    pass

@task
def setup_docker():
    # Check if docker exists else download it.
    with settings(warn_only=True):
        dockerExists = run("command -v apt")

        if dockerExists.failed:
            dockerInstall = _install_docker()

            if dockerInstall.failed:
                print(dockerInstall.stderr.split())
                return
        
        print("Docker successfully installed.")


@task
def pull_image():
    commands = "docker pull "
    result = run("uname -s")
    print(result.stdout.strip())

@task
def run_container():
    pass

@task 
def setup_aws_creds():
    creds = {
        "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
        "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"] 
    }

    for cred in creds:
        command = "export" + cred + "=" + creds[cred]
        with settings(warn_only=True):
            cmdExec = run(command)

            if cmdExec.succeeded:
                print(cred, " successfully setup on ec2 instance.")

@task 
def authenticate_docker():
    count = 0
    command = "eval $(aws ecr get-login --region us-west-2 --no-include-email)"

    def auth(command, count):
        cmdExec = ""
        
        if count < 1:
            with settings(warn_only=True):
                cmdExec = run(command)

                if cmdExec.succeeded:
                    command = cmdExec.stdout
                    count += 1
                    return auth(command, count)

        return cmdExec

    return auth(command, count)

def _install_docker():
    install_docker_commands = [
        "sudo yum update -y",
        "sudo yum install -y docker",
        "sudo service docker start",
        "sudo usermod -a -G docker ec2-user"
        ]

    cmdExec = ""
    
    # Execute command
    for command in install_docker_commands:
        isSudo = command.split(" ")[0] == "sudo"
        
        with settings(warn_only=True):
            if isSudo:
                cmdExec = sudo(command)
            else:
                cmdExec = run(command)

            if cmdExec.failed:
                return cmdExec
    
    return cmdExec