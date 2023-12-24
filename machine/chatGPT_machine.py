import openai
import configparser
import os

#openai.api_key = "" 

dialogs = ""
messages = []


class ChatMachine:

    def __init__(self, key="local"):
        self.openai = openai
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.openai.api_key = config['OPENAI']['key']
        print(self.openai.api_key)

    def get_analysis_result(self, actual_data, predictd_data):
        prompt = ("다음은 실제 가격 데이터야.\n" + actual_data + "\n" + "다음은 예측 가격 데이터야.\n" + predictd_data + "\n\n" 
        + "두 데이블을 비교해서 예측 가격 테이블이 실제 가격테이블의 추세를 잘 파악하는지 분석해줘. 너가 입력 받은 데이터를 테이블  형식으로 전환해서 반환해주고 id값은 테이블에서 빼줘. 구현 코드도 필요 없어. 모든 답변은 한국어로 해줘. 시작멘트와 끝멘트좀 하지마! 오직 답변만 해줘.")

        print(prompt)
        print(len(prompt))
        res = ""

        if prompt != "":
            messages.append({"role": "user", "content": prompt})
            completion = self.openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            #print(completion)
            res = completion.choices[0].message['content']
            #res = completion.choices[0].message['content'].replace("\n", "<br/>").replace(" "," &nbsp;" )
            messages.append({"role": 'assistant', "content": res}  )
            #print(res)
        
        return res