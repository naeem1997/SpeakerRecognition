from __future__ import print_function
from flask import Flask, json, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from UploadForm import UploadForm
import time, boto3, requests, json, urllib.request, os
# Does not work on EC2
# from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
import random
import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

s3 = boto3.client(
   "s3",
   #aws_access_key_id = S3_KEY,
   #aws_secret_access_key = S3_SECRET
)

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = set(['mp3', 'wav'])

app = Flask('__name__')

# Initialize MYSQL
mysql = MySQL(app)
app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Initialize the app for use with this MySQL class
# mysql.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file_to_s3(file, filename, acl):

    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            filename, #this will be the route the file is stored in -> myS3Bucket/myBucketName/filename
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return "{}{}".format(S3_LOCATION, filename)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/aws', methods=['GET', 'POST'])
def aws():
    form = UploadForm(request.form)
    # check if the post request has the file part
    if request.method == "POST" and form.validate():
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        # the file is stored here
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # All submitted form data can be forged, and filenames can be dangerous.
            # Secure them before adding to filesystem
            fileName = secure_filename(file.filename)
            fileContentType = file.content_type

            #the actual filename from the uploaded file
            print("Filename: " + fileName)
            print("fileContentType: " + fileContentType)
            userName = form.userName.data
            fileDescription = form.fileDescription.data
            print("userName: " + userName)
            #return redirect(url_for('uploadAudioFile', filename=filename))

            # Temporary - replace with a SQL query and do an s3id++ to increment id value by 1
            # Format to Create ID and store in MySQL: "S3_xxxxxx"
            fileURL = str(upload_file_to_s3(file, fileName, acl="private"))
            print(fileURL)
            # transcript = uploadAudioFile(fileURL, fileName, fileContentType)

            transcriptData = {}
            # transcriptData["transcript"] = transcript
            transcriptData["fileName"] = fileName
            transcriptData["fileDescription"] = fileDescription
            transcriptData["userName"] = userName

            # MySQL cursor to execute commands
            # Compatable with the flaskext.mysql module
            cur = mysql.get_db().cursor()

            # Check to see if the user exists already
            result = cur.execute("SELECT * FROM users WHERE username = %s", [userName])

            # User Does not Exist - so add to DB
            if result == 0:
                # Execute MySQL
                cur.execute("INSERT INTO users(username) VALUES (%s)", [userName])
                # Commit
                mysql.get_db().commit()
                # Close connection cursor
                cur.close()

            return(render_template('transcript.html', transcriptData=transcriptData))
        return(render_template('aws.html', form=form))
    return(render_template('aws.html', form=form))



def getRequest(fileURL):
    transcript = requests.get(fileURL).json()
    print("Type: " + str(type(transcript)))
    print("\nThe Transcript: \n  " + transcript['results']['transcripts'][0]['transcript'])
    return transcript['results']['transcripts'][0]['transcript']


if __name__ == '__main__':
    app.secret_key = 'itsNotASecretIfItsInVersionControl' # TODO: Figure out how to put this in the config file
    app.run(host="0.0.0.0", port=5000, debug = True)
