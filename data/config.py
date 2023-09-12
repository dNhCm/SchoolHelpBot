
from configparser import ConfigParser
import os


config = ConfigParser()
path = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])
config.read(f'{path}/config.ini', encoding='UTF-8')
