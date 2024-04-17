#referenced documentation sample code here https://thingsboard.io/docs/reference/python-rest-client/
import logging
import configparser
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException
from json import dumps

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def main():
    config = readConfig()
    url = config['Config']['private_url']
    # Creating the REST client object with context manager to get auto token refresh
    with RestClientCE(base_url=url) as rest_client:
        try:
            # Auth with credentials
            rest_client.login(username=config['Auth']['tenant_user'], password=config['Auth']['tenant_password'])

            # Creating a Device
            default_device_profile_id = rest_client.get_default_device_profile_info().id
            device = Device(name="api generated device", device_profile_id=default_device_profile_id)
            device = rest_client.save_device(device)

            logging.info(" Device was created:\n%r\n", device)
            rest_client.provision_device(config, "dev1")
        except ApiException as e:
            logging.exception(e)

#parse config and return config object
def readConfig():
    config = configparser.ConfigParser()
    config.read('configurations.ini')
    return config

if __name__ == '__main__':
    main()