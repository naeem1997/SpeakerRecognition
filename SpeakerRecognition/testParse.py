import time
import boto3
import datetime
import json


def open_and_parse():

    with open('transcriptedFileData.json') as f:
        data = json.load(f)

    result_obj = data['results']
    result_obj = result_obj['transcripts']
    result_obj = result_obj[0]
    print("\nThe Transcript: ")
    print(result_obj['transcript'])


#    result_obj = data['results']["speaker_labels"]["segments"][0]


    # itemNumber = 0
    # contentNumber = itemNumber
    # startTimeArray = []
    # # get the start time listed in the json response of each utterance
    # for k in result_obj["items"]:
    #     #print(result_obj["items"][itemNumber]["start_time"])
    #     startTimeArray.append(result_obj["items"][itemNumber]["start_time"])
    #     itemNumber = itemNumber + 1
    #
    # itemNumber = 0
    # contentList = []
    # #get the content associated with the above response time
    # for k in startTimeArray:
    #     if 'None' not in str(data['results']["items"][itemNumber]["alternatives"][0]["confidence"]):
    #         content = data['results']["items"][itemNumber]["alternatives"][0]["content"]
    #         contentList.append(content)
    #     else:
    #         itemNumber = itemNumber + 1
    #         content = data['results']["items"][itemNumber]["alternatives"][0]["content"]
    #         contentList.append(content)
    #     itemNumber = itemNumber + 1
    #
    # int = 0
    # for k in startTimeArray:
    #     print(k + "s: " + contentList[int])
    #     int = int + 1
