from datetime import datetime
import time
import os

from dateutil.tz import tzlocal
import paramiko
from boto3.session import Session

## importing the load_dotenv from the python-dotenv module
from dotenv import load_dotenv
 
## using existing module to specify location of the .env file
from pathlib import Path
import os
 

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

session = Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                  region_name=os.getenv("REGION"))


def deploy():
    # Amazon Linux AMI PV Instance Store 64-bit
    ami_id = 'ami-00dfe2c7ce89a450b'
    instance_type = 't2.nano'

    prices = {'m1.small': 0.044}

    ec2 = session.resource('ec2')
    client = session.client('ec2')

    private_key_file = os.path.abspath('keys/{0}.pem'.format(os.getenv("KEY_PAIR_NAME")))

    print(private_key_file)
    if not os.path.isfile(private_key_file):
        print('Creating new keys')
        key = client.create_key_pair(KeyName=os.getenv("KEY_PAIR_NAME"))
        with open(private_key_file, 'w') as f:
            f.write(key['KeyMaterial'])

    instances = [instance for instance in ec2.instances.all() if instance.state['Name'] != 'terminated']

    if not instances:
        ec2.create_instances(ImageId=ami_id,
                             MinCount=1,
                             MaxCount=1,
                             KeyName=os.getenv("KEY_PAIR_NAME"),
                             InstanceType=instance_type)

    while not [instance for instance in ec2.instances.all() if instance.state['Name'] == 'running']:
        time.sleep(5)

    instance = instances[0]
    print('ssh -i {0} ec2-user@{1}'.format(private_key_file, instance.public_ip_address))

    print(instance.id, instance.instance_type, instance.state,
          round((datetime.now(tzlocal()) - instance.launch_time).seconds / 60 / 60 * prices[instance.instance_type], 3),
          instance.public_dns_name, instance.public_ip_address)

    print(instance.security_groups[0]['GroupId'])
    security_group = ec2.SecurityGroup(instance.security_groups[0]['GroupId'])
    ssh_permission = [permission for permission in security_group.ip_permissions
                      if 'ToPort' in permission and permission['ToPort'] == 22]

    if not ssh_permission:
        security_group.authorize_ingress(IpProtocol='tcp', FromPort=22, ToPort=22, CidrIp='0.0.0.0/0')

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(instance.public_ip_address, username='ec2-user', key_filename=private_key_file)


if __name__ == '__main__':
    deploy()