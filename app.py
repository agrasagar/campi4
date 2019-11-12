import argparse
from flask import Flask
from flask import Response, request, make_response, send_file, abort
from cam import Cam

app = Flask(__name__)

apiDesHtml = ("<h1>GET:</h1>"
        "<h2>/snap/cam_number?:imageName&:colorSpace</h2>"
        "<p>cam_number (required): is the port where the "
        "cam in PI is jacked in (possible values = 0, 1, 2 ,3);</p>"
        "<p>imageName: name of image must have ext .jpg</p>"
        "<p>colorSpace(opt): supported values are RGB, HSV and YUV</p>"
        "<p>NOTE: only .jpg images are returned by the camera app</p>"
        "<h3>example:</h3><p>http://192.168.10.47:5000/snap/0?colorSpace=RGB</p>"
        "<p>http://192.168.10.47.5000/snap/0?imageName=test_011.jpg</p>"
        )

@app.route('/')
def index():
    return Response(response=apiDesHtml, status=200, content_type='text/html')

@app.route('/snap/<cam_number>', methods=['GET'])
def get_snap(cam_number):
    cam = Cam("mecCam")
    colorSpace = request.args.get('colorSpace'
                                , default="RGB"
                                , type = str)
    colorSpace = colorSpace.upper()
    if colorSpace not in cam.supported_colorspace:
        return Response(response="colorSpace {} is not supported".format(colorSpace)
                    , status=400)
    status, retStr = cam.take_snap(cam_number, colorSpace)
    if status == "SUCCESS":
        image_filename = retStr
        attachment_name = request.args.get('imageName'
                                            , default=image_filename
                                            , type = str)
        if ".jpg" not in attachment_name[-4:]:
            return Response(response="Only .jpg image can be expected."
                        , status=400)
        response = make_response(send_file(image_filename
                                        , as_attachment=True
                                        , attachment_filename=attachment_name))
    else:
        if "Cannot identify" in retStr:
            hw_miss_resp = "Camera is not on PI port {}.".format(cam_number)
            response = Response(response=hw_miss_resp, status=512)
        elif "PERMISSION DENIED" in retStr.upper():
            response = Response(response="Enable Camera in PI conig.", status=512)
        else:
            response = Response(response=retStr, status=500)
    return response


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", help="ip for the app", default="0.0.0.0", type=str)
    ap.add_argument("-p",  help= "port for the app", default=5994, type=int)
    args = vars(ap.parse_args())
    app.run(debug=True, port=int(args['p']), host=args['i'])
