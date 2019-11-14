import argparse
from flask import Flask
from flask import Response, request, make_response, send_file, render_template, redirect

from cam import Cam
from swagger import initialize_swagger


app = Flask(__name__)
initialize_swagger(app)

@app.route('/')
def index():
    return redirect('/swagger/', code=302)

@app.route('/snap/<cam_number>', methods=['GET'])
def get_snap(cam_number):
    if not cam_number.isdigit() or int(cam_number) not in range(0,20):
        return render_template('errors_basic.html'
                            , code=400
                            , error="Video device id {} not supported".format(cam_number))
    cam = Cam("mecCam")
    colorSpace = request.args.get('colorSpace'
                                , default="RGB"
                                , type = str)
    colorSpace = colorSpace.upper()
    if colorSpace not in cam.supported_colorspace:
        return render_template('errors_basic.html'
                            , code=400
                            , error="colorSpace {} is not supported".format(colorSpace))
    status, retStr = cam.take_snap(cam_number, colorSpace)
    if status == "SUCCESS":
        image_filename = retStr
        attachment_name = request.args.get('imageName'
                                            , default=image_filename
                                            , type = str)
        if ".jpg" not in attachment_name[-4:]:
            error_str="Only .jpg image can be expected."
            error_code = 400
            response = make_response(render_template('errors_basic.html'
                            , error=error_str), error_code)
        else:
            response = make_response(send_file( image_filename
                                    , as_attachment=True
                                    , attachment_filename=attachment_name
                                    , cache_timeout=0), 200)
    else:
        if "Cannot identify" in retStr:
            error_str="Camera is not on PI port {}.".format(cam_number)
            error_code = 512
        elif "PERMISSION DENIED" in retStr.upper():
            error_str="Enable Camera in PI conig."
            error_code = 512
        elif "SystemError" in retStr:
            error_str="dev id is wrong."
            error_code=512
        else:
            error_str = retStr
            error_code = 500
        rendered = render_template('errors_basic.html', error=error_str)
        response = make_response(rendered, error_code)
    return response


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", help="ip for the app", default="0.0.0.0", type=str)
    ap.add_argument("-p",  help= "port for the app", default=5994, type=int)
    args = vars(ap.parse_args())
    app.run(debug=False, port=int(args['p']), host=args['i'])
