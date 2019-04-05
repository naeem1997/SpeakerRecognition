# --------------------------------------------------------------------
# The returning JSON reponse from AWS Transcribe is a mess.
# This application parses the JSON response to seperate the transcript by speaker
# It identifies the indivual words spoken by each speaker
# To do this, the words were cross referenced by time
# The most confident word was chosen, as per the confidence index
# --------------------------------------------------------------------

import json, datetime
from datetime import datetime
def convertJsonToSRT(data):
    finalList = []
    #file = "asrOutput2.json"
    #data = json.load(open(file))

    # Each segment begins with:
    #       - the speaker start_time
    #       - the speaker_label
    #       - the end_time
    #       - items -  a list of the same information as above - broken down by utterance
    for segment in data['results']['speaker_labels']['segments']:

        if len(segment['items']) > 0:

            # Format the begining of each segment
            #
            segmentList = []
            # Convert AWS time format to datetime format
            # Example -> 3.04 becomes 00:03
            # Example -> 77.04 becomes 01:17
            segmentList.append(datetime.fromtimestamp(float(segment['start_time'])).strftime("%M:%S"))
            segmentList.append(" -- ")
            segmentList.append((str(segment['speaker_label'])))
            segmentList.append(": ")

            # Loop through each word item to get the result
            # Reference the JSON API to see structure
            for word in segment['items']:
                for result in data['results']['items']:
                    # if there was a word spoken in that time frame
                    if result['type'] == 'pronunciation':
                        # see if the start times match up
                        if result['start_time'] == word['start_time']:

                            # Sometimes more than one word is returned
                            # This occurs when AWS does not have high confidence in the word
                            # In this case, get the highest rated word
                            # If there is a word:
                            if len(result['alternatives']) > 0:
                                current_word = dict()
                                confidence_scores = []
                                for score in result['alternatives']:
                                    confidence_scores.append(score['confidence'])
                                for alternative in result['alternatives']:
                                    # get the max value of the list
                                    if alternative['confidence'] == max(confidence_scores):
                                        current_word = alternative.copy()
                                try:
                                    # add a space between words, but before appending
                                    # because of punctuation
                                    segmentList.append(" ")
                                    segmentList.append(current_word['content'])

                                    possiblePunctuation = data['results']['items'][data['results']['items'].index(result) + 1]['type']
                                    # There is indeed a punctuation mark
                                    if possiblePunctuation == 'punctuation':
                                        actualPunctuation = data['results']['items'][data['results']['items'].index(result) + 1]['alternatives'][0]['content']
                                        segmentList.append(actualPunctuation)
                                except:
                                    pass

        segmentList.append("/")
        spokenLine = ""
        for val in segmentList:
            if(val != "/"):
                spokenLine += val
            else:
                finalList.append(spokenLine)

    return finalList


if __name__ == '__main__':
    convertJsonToSRT()
