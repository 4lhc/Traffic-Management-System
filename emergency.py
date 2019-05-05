
from time import sleep
import requests


ip = "192.168.1.110"
ip = "0.0.0.0"
port = "5000"
url = 'http://{}:{}/emergency_clear_route'.format(ip, port)

def main():
    r = requests.get(url = url)


if __name__ == '__main__':
    main()
