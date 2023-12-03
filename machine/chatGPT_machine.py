from flask import Flask, request
import openai
import os

#openai.api_key = "" 

dialogs = ""
messages = []


class ChatMachine:

    def __init__(self, key="local"):
        self.openai = openai
        self.openai.api_key = ""

    def get_analysis_result(self, actual_data, predictd_data):

        prompt = ("다음은 실제 가격 데이터야.\n" + actual_data + "\n" + "다음은 예측 가격 데이터야.\n" + predictd_data + "\n\n" 
        + "두 데이블을 비교해서 예측 가격 테이블이 실제가격테이블의 추세를 잘 파악하는지 분석해줘. 전반적인 추세만 알려줘 정확성은 필요 없어. 구현 코드도 필요 없어. \n\n" 
        + """답변은 다음과 같은 형식으로 해줘. \n\n 예측 가격 테이블과 실제 가격 테이블의 추세를 비교하여 전반적인 추세를 분석합니다.\n\n
        먼저, 예측 가격 테이블의 'predicted_price' 값을 차례대로 확인하여 전체적인 추세를 분석할 수 있습니다.\n\n
        예측 가격 테이블의 'predicted_price' 값은 다음과 같습니다.\n
        [49991264.0, 50456228.0, 50630756.0, 49777376.0, 48943784.0, 49196528.0, 49830016.0, 49030872.0, 49157744.0, 48782848.0, 49256452.0, 48144672.0, 48999032.0, 49465652.0, 49302412.0]\n
        실제 가격 테이블의 'close_price' 값을 차례대로 확인하여 전체적인 추세를 분석할 수 있습니다.\n
        실제 가격 테이블의 'close_price' 값은 다음과 같습니다.\n
        [50087000, 50429000, 50595000, 49779000, 49025000, 49218000, 49788000, 48992000, 49128000, 48683000, 49212000, 48238000, 49075000, 49576000, 49576000]\n
        두 가격 테이블을 비교하여 전반적인 추세를 분석하면 다음과 같습니다.\n
        - 11월 13일부터 11월 16일까지는 실제 가격과 예측 가격이 유사한 추세를 보입니다.\n
        - 11월 17일부터 11월 18일까지 실제 가격과 예측 가격이 다른 추세를 보입니다.\n
        - 11월 19일부터 11월 21일까지 실제 가격과 예측 가격이 다른 추세를 보입니다.\n
        - 11월 22일부터 11월 25일까지 실제 가격과 예측 가격이 유사한 추세를 보입니다.\n
        - 11월 26일부터 11월 27일까지 실제 가격과 예측 가격이 다른 추세를 보입니다.\n
        전반적으로는 예측 가격 테이블의 추세가 실제 가격 테이블의 추세를 일정 부분 파악할 수 있습니다. 그러나 특정 기간에는 예측 가격과 실제 가격이 다른 추세를 보이기도 합니다. 이를 종합적으로 분석하면 전체적인 추세는 비슷하지만 정확성은 필요할 수 있음을 알 수 있습니다.""")
        print(prompt)
       
        res = ""

        if prompt != "":
            messages.append({"role": "user", "content": prompt})
            completion = self.openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            #res = completion.choices[0].message['content']
            res = completion.choices[0].message['content'].replace("\n", "<br/>").replace(" "," &nbsp;" )
            messages.append({"role": 'assistant', "content": res}  )
            print(res)
        
        return res