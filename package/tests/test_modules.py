import sys 
sys.path.append('..')
import os
import pytest
import modules.database as database
import modules.ldap as ldap
import modules.pingdevice as pingdevice
from modules.assorted import getLocation, getGroup, compare, Config
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from modules.database import Base, Table

class extensionAttribute2:
    def __init__(self):
        self.values = (0,)
        self.value = 'unknown'

class Device:
    def __init__(self):
        self.value = 0
        self.name = 'localhost'
        self.extensionAttribute2 = extensionAttribute2()
        self.distinguishedName = 'CN=CTVM01,OU=Early Updates,OU=Computers,DC=internal,DC=contoso,DC=com'

device = Device()

config = Config()


def test_compare_false():
    assert compare([1,2,3],[3,4,5]) == False

def test_compare_true():
    assert compare([1,2,3],[4,5,6]) == True

def test_getLocation():
    assert getLocation(device,'10.0.0',config.parameter['subnet_dict']) == "Contoso"

def test_getGroup():
    assert getGroup(device) == 'Early Updates'

def test_pingdevice():
    ping_result_ip, ping_result_time, subnet_ip, ping_returncode = pingdevice.ping(device.name)
    assert ping_result_ip == '127.0.0.1'
    assert subnet_ip == '127.0.0'
    assert ping_returncode == 0
    
def test_Database():
    engine, connection, session, metadata = database.connect_db(config.parameter['database'])
    data = [{'id': str('test123'),
             'ip': str('127.0.0.1'),
             'ping_code': int(0),
             'ping_time': float(0),
             'time_stamp': str('0000-1111'),
             'description': str('Description'),
             'location': str('Location'),
             'group': str('Group'),
             'tv': str('TV'),
             'lastlogon': str('0000-1111'),
             'os': str('OS'),
             'version': str('Ver')},]
    session.bulk_insert_mappings(Table, data)
    try:
        session.commit()
        assert True
    except:
        session.rollback()
        assert False
    os.remove(config.parameter['database'])
