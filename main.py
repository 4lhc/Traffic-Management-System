from TMS.density import Density
from time import sleep


def main():
    stream_url = 'http://0.0.0.0:5000/video_feed'
    d = Density(stream_url)
    d.begin_processing()

    while True:
        print("density = {}".format(d.density))
        sleep(2)



if __name__ == '__main__':
    main()
