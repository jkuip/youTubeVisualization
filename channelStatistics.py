import urllib.request
import json
import csv
import operator
import re
import datetime

def convertToDays(duration):
    return str(datetime.timedelta(seconds=duration))

def convertToSeconds(duration):
    a = re.findall(r'\d+', duration)
    seconds = 0
    if 'H' in duration and 'M' in duration and 'S' in duration:
        seconds = int(a[0]) * 3600 + int(a[1]) * 60 + int(a[2])
    elif 'H' not in duration and 'M' in duration and 'S' in duration:
        seconds = int(a[0]) * 60 + int(a[1])
    elif 'H' not in duration and 'M' not in duration and 'S' in duration:
        seconds = int(a[0])
    elif 'H' not in duration and 'M' in duration and 'S' not in duration:
        seconds = int(a[0]) * 60
    return seconds

# youtube channel - place your youtube channelID below
channelID = 'UC_abc123'

# youtube API key - get yours at: https://console.developers.google.com/
API_KEY = 'abc123'

# get basic channel info
url = 'https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&id=' + channelID + '&key=' + API_KEY
req = urllib.request.Request(url)
response = urllib.request.urlopen(req)
results = json.load(response)

# get channel name
channelName = results['items'][0]['snippet']['localized']['title']
channelNameFormatted = channelName.replace(" ", "").lower()

# get basic channel statistics
viewCount = results['items'][0]['statistics']['viewCount']
videoCount = results['items'][0]['statistics']['videoCount']
subscriberCount = results['items'][0]['statistics']['subscriberCount']

# create a new spreadsheet
myFile = open(channelNameFormatted + '.csv', 'w', encoding='utf-8')
with myFile:
    myFields = ['videoId', 'title', 'date', 'seconds']
    writer = csv.DictWriter(myFile, fieldnames=myFields)
    writer.writeheader()
    
# get all channel videos
baseUrl = 'https://www.googleapis.com/youtube/v3/search?key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(API_KEY,channelID)
channelUrl = baseUrl

# initialize statistics
totalSeconds = 0
totalLikes = 0
totalComments = 0

# loop through each video
while True:
    channelResponse = urllib.request.urlopen(channelUrl)
    channelResults = json.load(channelResponse)
    
    # get the duration of each video
    for i in channelResults['items']:
        if i['id']['kind'] == 'youtube#video' or i['id']['kind'] == 'youtube#searchResult':
            videoId = i['id']['videoId']
            videoDetailsUrl = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id=' + videoId + '&key=' + API_KEY
            videoResponse = urllib.request.urlopen(videoDetailsUrl)
            videoResults = json.load(videoResponse)
            videoDuration = videoResults['items'][0]['contentDetails']['duration']
            videoSeconds = convertToSeconds(videoDuration)
            
            # print title & video duration
            print(i['snippet']['title'])
            print(str(videoSeconds) + ' seconds')
            print('--------------------')
            
            # update statistics
            totalSeconds = totalSeconds + videoSeconds
            try:
                totalLikes = totalLikes + int(videoResults['items'][0]['statistics']['likeCount'])
            except KeyError:
                continue
            try:
                totalComments = totalComments + int(videoResults['items'][0]['statistics']['commentCount'])
            except KeyError:
                continue
                
            # append video data to the spreadsheet
            myFile = open(channelNameFormatted + '.csv', 'a', encoding='utf-8')
            with myFile:
                writer = csv.DictWriter(myFile, fieldnames = myFields)
                writer.writerow(
                {
                    'videoId': i['id']['videoId'],
                    'title': i['snippet']['title'],
                    'date': i['snippet']['publishedAt'],
                    'seconds': videoSeconds
                })
    try:
        nextPageToken = channelResults['nextPageToken']
        channelUrl = baseUrl + '&pageToken={}'.format(nextPageToken)
    except:
        break;
        
# reverse sort csv file
data = csv.reader(open(channelNameFormatted + '.csv'), delimiter=',')
header = next(data, None)
sortedlist = sorted(data, key=operator.itemgetter(2))
with open(channelNameFormatted + '.csv', 'w') as f:
    fileWriter = csv.writer(f, delimiter=',')
    if header:
        fileWriter.writerow(header)
    fileWriter.writerows(sortedlist)
            
# print channel statistics
print(channelName)
print('Total Seconds: {}' . format(totalSeconds))
print('Total Time: {}' . format(convertToDays(totalSeconds)))
print('Total Likes: {}' . format(totalLikes))
print('Total Comments: {}' . format(totalComments))
print('Subscribers: {}' . format(subscriberCount))
print('Views: {}' . format(viewCount))
print('Videos: {}' . format(videoCount))