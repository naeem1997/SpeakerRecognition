# --------------------------------------------------------------------
# The returning JSON reponse from AWS Transcribe is a mess.
# This application parses the JSON response to show the confidence scores of the response
# In the JSON, every word comes with a confidence scores
# This file sums the confidence score occurances within a range
# --------------------------------------------------------------------
import statistics

def get_stats_from_json(data):

    statsDictionary = {
            'accuracy': [],
            '10': 0, '9.8': 0, '9': 0, '8': 0, '7': 0, '6': 0, '5': 0, '4': 0, '3': 0, '2': 0, '1': 0, '0': 0,
            'total': len(data['results']['items'])
            }
    listOfStatistics = []
    for item in data['results']['items']:
        if item['type'] == 'pronunciation':

            statsDictionary['accuracy'].append(int(float(item['alternatives'][0]['confidence']) * 100))
            if float(item['alternatives'][0]['confidence']) >= 1: statsDictionary['10'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.9: statsDictionary['9'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.8: statsDictionary['8'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.7: statsDictionary['7'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.6: statsDictionary['6'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.5: statsDictionary['5'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.4: statsDictionary['4'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.3: statsDictionary['3'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.2: statsDictionary['2'] += 1
            elif float(item['alternatives'][0]['confidence']) >= 0.1: statsDictionary['1'] += 1
            else: statsDictionary['0'] += 1

    valueToPercentMapping = {"10" : "100%", "9": '90% - 99%', '8':'80% - 89%', '7':'70% - 79%', '6':'60% - 69%', '5': '50% - 59%', '4': '40% - 49%', '3':'30% - 39%', '2': '20% - 29%', '1': ' 10% - 19%', '0': '< 9%'}

    for i in range(10,-1,-1):
        tempList = []
        tempList.append(valueToPercentMapping[str(i)])
        tempList.append(statsDictionary[str(i)])
        tempList.append(str(round(statsDictionary[str(i)] / statsDictionary['total'] * 100, 2)) + '%')
        listOfStatistics.append(tempList)

    return listOfStatistics

if __name__ == '__main__':
    get_stats_from_json()
