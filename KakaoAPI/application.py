from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import train as TR


application = Flask(__name__)

news = "───────────────────────────────────────────\n\
[홈페이지]      2023-05-30\n\
신청·접수  >  내용검토  >  승인서 발부  >  촬영\n\
───────────────────────────────────────────\n\
[트위터]        2023-05-25\n\
안내말씀 드립니다.\n\
코레일 운영구간인 수인분당선 선로 장애로 왕십리역~선릉역 상하행 열차운행이 일시 중단되었으니, 환승 이용객들께서는 이 점 참고하여 열차를 이용해 주시기 바랍니다.\n\
자세한 사항은 코레일로 문의주시기 바랍니다.\n\
───────────────────────────────────────────\n\
[트위터]        2023-05-25\n\
안내말씀 드립니다.\n\
내일(21일) 오전 6시부터 11시까지 '2023 서울 자전거 대행진' 이 예정되어 있습니다.\n\
광화문역, 월드컵경기장역 주변이 다소 혼잡할 수 있고, 자전거 휴대승차 이용객이 많을 예정이니 이 점 참고하여 열차를 이용해 주시기 바랍니다.\n\
"
@application.route("/", methods=['POST'])
def keyword():
    req = request.get_json()
    text_ck = req["action"]["detailParams"]
    text_Mn = req['userRequest']['utterance']
    print(text_Mn)
    if text_Mn=="뉴스":
        print(news)
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": news
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
    
