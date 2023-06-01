from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import train as TR
import news as NS


application = Flask(__name__)


@application.route("/", methods=['POST'])
def keyword():
    req = request.get_json()
    text_ck = req["action"]["detailParams"]
    text_Mn = req['userRequest']['utterance']
    print(text_Mn)
    if text_Mn=="뉴스":
        Result = NS.NC_PrintNews(8)
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": Result
                        }
                    }
                ]
            }
        }
    else:
        text = req['userRequest']['utterance'].split(";")
        print(text_ck)
        Result = TR.MAINFUNC(text_ck['subwayLineNum']['value'], text[0], text[1], text_ck['updnLine']['value'])
        print(Result)
        # 답변 텍스트 설정
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": Result
                        }
                    }
                ]
            }
        }

    # 답변 전송
    print(res)
    return jsonify(res)


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)
    
