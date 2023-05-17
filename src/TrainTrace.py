from typing import Any
import requests
import json
import pyautogui

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
        print (DATA.jsonData[i],"\n")
        if(DATA.jsonData[i]["subwayId"] == subwayId and DATA.jsonData[i]["updnLine"] == updnLine):
            return DATA.jsonData[i]["btrainNo"]
        
def GLT_GetArrivalTime(destination, trainNum):  #도착 예정 시간 확인, 필요인자: 목적지, 리턴값: 남은 시간, 
    DATA = MU_GetJson("realtimeStationArrival", destination)
    for i in range (DATA.dataLength):
        if(DATA.jsonData[i]["btrainNo"] == trainNum):           
            output = trainLocation(DATA.jsonData[i]["barvlDt"], DATA.jsonData[i]["arvlMsg3"])  
            return output
        
if __name__ == '__main__':
    keyword=pyautogui.prompt('현재 지하철역을 입력해주세요')
    subwayNumber = GTN_GetTrainNum("1004", "상행", keyword)
    print(subwayNumber)
    
    timeTest = GLT_GetArrivalTime(keyword, subwayNumber)
    print("남은 시간: ",int(timeTest.lastTime)//60, "분 ", int(timeTest.lastTime)%60,"초", "\n현재 위치: ", timeTest.nowLocation)

    destination=pyautogui.prompt('도착 지하철역을 입력해주세요')
    timeTest = GLT_GetArrivalTime(destination, subwayNumber)
    print("남은 시간: ",int(timeTest.lastTime)//60, "분 ", int(timeTest.lastTime)%60,"초", "\n현재 위치: ", timeTest.nowLocation)

    
