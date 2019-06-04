import os
import sys

from common.ssh_utility import SSHUtil

from common.functions import get_config


def upload_code(ci_dir_path, source_path, des_path, service, cleanup):
    """
    Upload code to remote machine
    Example: upload_code ws/ci ws/dist/tenant.tar.gz /tmp/tenant.tar.gz
    :param ci_dir_path: CI folder path where all CI scripts are located
    :param source_path: Path the source code
    :param des_path: Destination folder to save the code
    :param service: backupservice or middleware
    :param cleanup: Execute cleanup scripts or not (True or False)
    :return: Output with status True or False
    """
    # Get master details from Yaml file
    yaml_file_path = os.path.join(ci_dir_path, 'config.yaml')
    server_ip = get_config(service, 'SERVER_IP')
    server_username = get_config(service, 'SERVER_USERNAME')
    server_pwd = get_config(service, 'SERVER_PASSWORD')


    # Connect to remote machine
    ssh_obj = SSHUtil(host=server_ip, username=server_username,
                      password=server_pwd, timeout=10)

    # Add proxy
    command = """
    export http_proxy="http://10.131.236.9:3128"
    export https_proxy="https://10.131.236.9:3128" &&
    export PATH=$PATH:$https_proxy &&
    export PATH=$PATH:$http_proxy &&
    echo $http_proxy &&
    echo $https_proxy """
    result = ssh_obj.execute_command(command)

    return_value = ''
    for line in result['output'].readlines():
        return_value = return_value + line
    print('############################')
    print("Proxy settings  info")
    print(return_value)

    # Clearing the existing tar.gz files in remote machine
    command = """cd /home/tas/ && sudo rm -rf *.gz"""
    result = ssh_obj.execute_command(command)


    # Upload code to remote machine
    ssh_obj.upload_file(source_path, des_path)

    # Upload installation shell script into remote machine
    installation_scripts = get_config(service, 'INSTALLATION_SCRIPT',
                                      )

    if cleanup == 'True':
        stop_service_list = get_config(service, 'STOP_SERVICES')
        # Stop the service
        for process in stop_service_list:
            command = "sudo systemctl stop {}".format(process)
            ssh_obj.execute_command(command)
            print('{} has been stopped'.format(process))


if __name__ == '__main__':
    ci_dir_path = sys.argv[1]
    source_path = sys.argv[2]
    des_path = sys.argv[3]
    service = sys.argv[4]
    cleanup = sys.argv[5]
    upload_code(ci_dir_path, source_path, des_path, service, cleanup)