from typing import Any
import requests
import json
import pyautogui
import sys
import base64


class trainData:
    def __init__(self, jsonData, dataLength):
        self.jsonData = jsonData
        self.dataLength = dataLength

class trainLocation:
    def __init__(self, lastTime, nowLocation):
        self.lastTime = lastTime
        self.nowLocation = nowLocation

def MU_GetJson(apiName, keyword):
    api_key = "637862555675726f34354b695a4d54"
    url = f"http://swopenapi.seoul.go.kr/api/subway/{api_key}/json/{apiName}/0/999/{keyword}"
    response = requests.get(url, headers={"Content-Type": "application/json; charset=utf-8", "Authorization": api_key})
    output = trainData(json.loads(response.text)["realtimeArrivalList"], len(json.loads(response.text)["realtimeArrivalList"])) 
    return output   

def GTN_GetTrainNum(subwayId, updnLine, station):  #열차 차량번호 얻기, 필요인자: 호선정보, 상하행선 정보, 지하철역
    DATA = MU_GetJson("realtimeStationArrival", station)
    for i in range (DATA.dataLength):
        if(DATA.jsonData[i]["subwayId"] == subwayId and DATA.jsonData[i]["updnLine"] == updnLine):
            return DATA.jsonData[i]["btrainNo"]
        
def GLT_GetArrivalTime(destination, trainNum):  #도착 예정 시간 확인, 필요인자: 목적지, 리턴값: 남은 시간, 
    DATA = MU_GetJson("realtimeStationArrival", destination)
    for i in range (DATA.dataLength):
        if(DATA.jsonData[i]["btrainNo"] == trainNum):           
            output = trainLocation(DATA.jsonData[i]["barvlDt"], DATA.jsonData[i]["arvlMsg3"])  
            return output
        
if __name__ == '__main__':
    subwayLineNum = sys.argv[1]
    startStation = sys.argv[2]
    destinationStation = sys.argv[3]
    subwayNumber = sys.argv[4]
    if(subwayNumber=='0'):
        subwayNumber = GTN_GetTrainNum(subwayLineNum, "상행", startStation)
        timeTest1 = GLT_GetArrivalTime(startStation, subwayNumber)
        # print("남은 시간: ",int(timeTest1.lastTime)//60, "분 ", int(timeTest1.lastTime)%60,"초", ";현재 위치: ", timeTest1.nowLocation,";", end='')
        timeTest2 = GLT_GetArrivalTime(destinationStation, subwayNumber)
        # print("남은 시간: ",int(timeTest2.lastTime)//60, "분 ", int(timeTest2.lastTime)%60,"초", ";현재 위치: ", timeTest2.nowLocation, end='')
        if(type(timeTest1)=='NoneType'):
            timeTest1.lastTime = 0
            print(0,";",timeTest2.lastTime,";",timeTest2.nowLocation, end=';')
        elif(type(timeTest2)=='NoneType'):
            timeTest2.lastTime = 0
            print(0,";",0,";",timeTest2.nowLocation, end=';')
        else:
            print(timeTest1.lastTime,";",timeTest2.lastTime,";",timeTest2.nowLocation, end=';')
    else:
        timeTest1 = GLT_GetArrivalTime(startStation, subwayNumber)
        timeTest2 = GLT_GetArrivalTime(destinationStation, subwayNumber)
        if(type(timeTest1)=='NoneType'):
            print(0,";",timeTest2.lastTime,";",timeTest2.nowLocation, end=';')
        elif(type(timeTest2)=='NoneType'):
            print(0,";",0,";",timeTest2.nowLocation, end=';')
        # print("남은 시간: ",int(timeTest2.lastTime)//60, "분 ", int(timeTest2.lastTime)%60,"초", ";현재 위치: ", timeTest2.nowLocation, end='')
        else:
            print(timeTest1.lastTime,";",timeTest2.lastTime,";",timeTest2.nowLocation, end=';')
    print(subwayLineNum,";",startStation,";",destinationStation,";",subwayNumber, end='')
