from TMS.density import Density
from time import sleep
import requests

DEMO_MODE = True

ip = "192.168.1.110"
port = "5000"
url = 'http://{}:{}'.format(ip, port)

def main():
    stream_url = url + '/video_feed'
    d = Density(stream_url)
    t = d.begin_processing()

    while t.isAlive():
        print("density = {}".format(d.density))
        traffic_ctrl_url = url + '/set_traffic_light'
        parameters = {'cmd': 'turn_on', "traffic_light": d.get_max_density()}
        r = requests.get(url = traffic_ctrl_url, params = parameters)
        sleep(30)
        #pause to do demo
        if DEMO_MODE:
            input("Press Enter")



if __name__ == '__main__':
    main()
