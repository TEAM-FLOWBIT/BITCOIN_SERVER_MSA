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

        prompt = "다음은 실제 가격 데이터야.\n" + actual_data + "\n" + "다음은 예측 가격 데이터야.\n" + predictd_data + "\n\n" + "두 데이블을 비교해서 예측 가격 테이블이 실제가격테이블의 추세를 잘 파악하는지 분석해줘. 전반적인 추세만 알려줘 정확성은 필요 없어. 구현 코드도 필요 없어."
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