#to be run in RPI
from flask import Flask, render_template, request, Response
from camera import VideoCamera
import lights



app = Flask(__name__) #create an webapp/webserver object

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


"""
connect to the following URL
http://0.0.0.0:5000/set_traffic_light?cmd=turn_on&traffic_light=1
cmd = turn_on [OR turn_off]
traffic_light = 1 -> first light
traffic_light = 2 -> second light
.
.
and so on
"""
@app.route("/set_traffic_light", methods=['GET', 'POST'])
def set_traffic_light():
    cmd  = request.args.get('cmd')
    traffic_light = request.args.get('traffic_light')

    if 'turn_on' in cmd:
        lights.turn_on(traffic_light)
        return "lights turn off"
    elif 'turn_off' in cmd:
        lights.turn_off(traffic_light)
        return "lights turn off"


@app.route("/emergency_clear_route")
def emergency_clear_route():
    """Stop traffic for emergency vehicle for passsing"""
    l = ["1", "2", "3", "4"]
    for i in l:
        lights.turn_off(i)

    return "Emergency"





if __name__ == "__main__":
    # ip_rpi = '192.168.1.107'
    ip_rpi = '0.0.0.0'
    app.run(host=ip_rpi, port=5000, debug=True)
