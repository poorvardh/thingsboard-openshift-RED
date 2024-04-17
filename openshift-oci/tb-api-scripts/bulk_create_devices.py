#referenced documentation sample code here https://thingsboard.io/docs/reference/python-rest-client/
import logging
import configparser
from tb_rest_client.rest_client_ce import *
from tb_rest_client.rest import ApiException

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    config = read_config()
    url = config['Config']['private_url']
    deviceNamePrefix = config['Config']['device_name_prefix']
    numDevicesToProvision = config['Config'].getint('num_devices_to_provision')
    
    # Creating the REST client object with context manager to get auto token refresh
    with RestClientCE(base_url=url) as rest_client:
        try:
            # Auth with credentials
            rest_client.login(username=config['Auth']['tenant_user'], password=config['Auth']['tenant_password'])
            token_file = open(config['Config']['token_file_name'], "w")
            for i in range(numDevicesToProvision):
                deviceName = deviceNamePrefix + str(i + 1)
                print(f'device name: {deviceName}')
                token = provisionDevice(config, deviceName)
                token_file.write(token)
                if i < numDevicesToProvision - 1:
                    token_file.write(",") #insert comma for csv format
            token_file.close()
        except ApiException as e:
            if token_file:
                token_file.close()
            logging.exception(e)

#parse config and return config object
def read_config():
    config = configparser.ConfigParser()
    config.read('configurations.ini')
    return config

def provisionDevice(config, deviceName:str):
    url = config['Config']['private_url_no_port']
    PROVISION_REQUEST = {"provisionDeviceKey": config['Auth']["provision_device_key"],
                        "provisionDeviceSecret": config['Auth']["provision_device_secret"],
                        "deviceName": deviceName,
                        }
    response = post("%s:%i/api/v1/provision" % (url, 8080), json=PROVISION_REQUEST)
    decoded_response = response.json()
    # print("Received response: ")
    # print(decoded_response)
    received_token = decoded_response.get("credentialsValue")
    return received_token

if __name__ == '__main__':
    main()