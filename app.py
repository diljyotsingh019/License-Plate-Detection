from utils import *
from logs import *
from config import *
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, Response, url_for # Used for web app deployments
from ultralytics import YOLO
import easyocr


logger = log_setup("main", LOGFILE)
app = Flask(__name__)

model = YOLO(MODELPATH)
reader = easyocr.Reader(['en'])

@app.route("/", methods = ["GET", "POST"])
def home():
    print(request.files)
    if "upload_image" in request.files:
        if secure_filename(request.files["upload_image"].filename) !="":
            file = request.files["upload_image"]
            file_name = secure_filename(file.filename)
            file.save(f"{IMAGEPATH}/{file_name}")
            image= detect_and_recognise(model, reader, cv2.imread(f"{IMAGEPATH}/{file_name}"))
            cv2.imwrite(f"{OUTPUT_PATH}/{file_name}", image) 
            return render_template("output_image.html", input_path = f"{IMAGEPATH}/{file_name}", output_path = f"{OUTPUT_PATH}/{file_name}")
        elif secure_filename(request.files["upload_video"].filename) !="":
            file = request.files["upload_video"]
            file_name = secure_filename(file.filename)
            file.save(f"{VIDEOPATH}/{file_name}")
            global cap
            cap = cv2.VideoCapture(f"{VIDEOPATH}/{file_name}")

            return render_template("output_video.html", input_path = f"{VIDEOPATH}/{file_name}")
        else:
            return render_template("home.html")
    else:
        return render_template("home.html")


# function to encode video frames
def GetVideo():

    # loop over frames from the output stream
    while True:

        ret, frame = cap.read()

        if ret:



            # detect the license and return the final frame with bounding box 
            final_frame = detect_and_recognise(model, reader, frame)


            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", final_frame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                    bytearray(encodedImage) + b'\r\n')

        else:
            break


# stream video to endpoints
@app.route("/video_stream")
def video_stream():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(GetVideo(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(debug= True)