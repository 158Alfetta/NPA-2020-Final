import netmiko

#Define device detail via DEVICE_PARAMS
DEVICE_PARAMS = {
                'device_type':'cisco_ios',
                'ip':"10.0.15.104",
                'username':'admin',
                'password':'cisco'
}

#set a Loopback interface when it's time to come
def setLbInt(device_params):
    ssh = netmiko.ConnectHandler(**device_params)
    result = ssh.send_config_set([
        'interface loopback 60070120',
        'ip address 192.168.1.1 255.255.255.0',
        'description testingNetmikoConfigLoopback'
        ])
    print(result)
    ssh.disconnect()
    
setLbInt(DEVICE_PARAMS)