import boto3


def upload_file():
    # Create an S3 client
    s3 = boto3.client('s3')

    filename = 'liveRecording.wav'
    bucket_name = '4485testasr'

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file(filename, bucket_name, filename)

    print("File " + filename + "uploaded to S3")

if __name__ == '__main__':
    # test1.py executed as script
    # do something
    upload_file()
