# --------------------------------------------------------------------
# The returning JSON reponse from AWS Transcribe is a mess.
# This application parses the JSON response to seperate the transcript by channel
# It identifies the indivual words spoken in each channel
# --------------------------------------------------------------------

import json, datetime
from datetime import datetime

# Each segment begins with:
#       - the channel label
#       - items -  a list of the same information as above - broken down by utterance
#       - refer to the docs for more information

def convertJsonToSRT(data):
    finalList = []
    spokenWords = []
    spokenWords.append("Speaker 1")
    for segment in data['results']['channel_labels']['channels']:
        for word in segment['items']:
            spokenWords = []
            for result in data['results']['items']:
                # if there was a word spoken in that time frame
                if result['type'] == 'pronunciation':
                    spokenWords.append(result['alternatives'][0]['content'])
                    spokenWords.append(" ")
            spokenWords.append("Speaker 2")

        spokenWords.append("/")
        spokenLine = ""
        for val in spokenWords:
            if(val != "/"):
                spokenLine += val
            else:
                finalList.append(spokenLine)

    return finalList

if __name__ == '__main__':
    convertJsonToSRT()
