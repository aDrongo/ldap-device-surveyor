import netaddr

from datetime import datetime
import time
import re
import os
import asyncio

from modules.logger import logging
from modules.config import config

subnets = config['subnet_dict']

def scan(devices):
    device_count = len(devices)
    logging.debug(f"Scanning {device_count}")
    start_time = time.monotonic()

    results = asyncio.run(main(devices))

    end_time = time.monotonic()
    logging.info(f'Completed {device_count} in {end_time - start_time} seconds')

    return results
    
async def main(devices):
    return await asyncio.gather(*[survey_device(device) for device in devices])

async def survey_device(device):
    ping_string, ping_code = await ping_device(device.id)
    device = interpret_ping_result(ping_string, ping_code, device)
    cur_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    device.time_stamp = cur_time
    if (device.ping_code == 0):
        device.lastup = cur_time
    return device

async def ping_device(device):
    if os.name == 'posix':
        ping_async = await asyncio.create_subprocess_exec(
            'ping',
            f'{device}',
            '-c 1',
            #'-4'
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
    elif os.name == 'nt':
        ping_async = await asyncio.create_subprocess_shell(
            f'ping {device} /4 /n 1', 
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE) 
    stdout, stderr = await ping_async.communicate()
    if stdout:
        ping_result = stdout.decode()
    elif stderr:
        ping_result = stderr.decode()
    ping_code = int(ping_async.returncode)
    if os.name == 'nt' and ping_code == 1:
        ping_code = 2
    return ping_result, ping_code

def interpret_ping_result(ping_result, ping_code, device):
    device.ping_code = ping_code
    if os.name == 'nt':
        if device.ping_code == 1:
            device.ping_code = 2
        if device.ping_code == 0 and "Destination host unreachable" in ping_result:
            device.ping_code = 1
    if device.ping_code == 0:
        device.ip = get_IP(ping_result)
        device.location = get_location(ping_result)
        device.ping_time = get_time(ping_result)
    else:
        device.location = 'Unknown'
        device.ip = '0.0.0.0'
        device.ping_time = '0.0'
    return device

def get_time(string):
    try:
        if os.name == 'posix':
            return str((re.search(r'time=\d+\.\d+', str(string))).group(0)).replace("time=","")
        elif os.name == 'nt':
            return str((re.search(r'time\D\d+', str(string))).group(0)).replace("time","").replace('=','').replace('<','')
    except:
        return '0.0'

def get_IP(string):
    try:
        return (re.search(r'\d+\.\d+\.\d+\.\d+', str(string))).group(0)
    except:
        return '0.0.0.0'

def get_location(string):
    ip = netaddr.IPAddress(get_IP(string))
    for key in subnets:
        if (ip in netaddr.IPNetwork(key)):
            return subnets[key]
    return 'Unknown'