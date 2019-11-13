import argparse
from flask import Flask
from flask import Response, request, make_response, send_file, render_template, redirect
from flask_restplus import Api

from cam import Cam
from swagger import initialize_swagger

app = Flask(__name__)
initialize_swagger(app)

@app.route('/')
def index():
    return redirect('/swagger/', code=302)

@app.route('/snap/<cam_number>', methods=['GET'])
def get_snap(cam_number):
    cam = Cam("mecCam")
    colorSpace = request.args.get('colorSpace'
                                , default="RGB"
                                , type = str)
    colorSpace = colorSpace.upper()
    if colorSpace not in cam.supported_colorspace:
        return render_template('errors_basic.html'
                            , code=400
                            , error="colorSpace {} is not supported".format(colorSpace) )
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
