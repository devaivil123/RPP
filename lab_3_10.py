import http.client

#Задание 1: Отправить HTTP запрос GET /number/{Вариант}.
import json

def operate(data: str, left: int):
    dict = json.loads(data)
    if dict['operation'] == 'sum':
        return left + int(dict['number'])
    if dict['operation'] == 'sub':
        return left - int(dict['number'])
    if dict['operation'] == 'mul':
        return left * int(dict['number'])
    if dict['operation'] == 'div':
        return left // int(dict['number'])

conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request('GET', '/number/10')
r1 = conn.getresponse()
print(r1.status, r1.reason)

data1 = r1.read().decode()
left = json.loads(data1)['number']
print(left)

#Задание 2:    Отправить HTTP запрос GET /number/ с параметром запроса option={Вариант}.
conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request('GET', '/number/?option=10')
r1 = conn.getresponse()
print(r1.status, r1.reason)

data1 = r1.read().decode()
left = operate(data1, left)
print(left)

#Задание 3: Отправить HTTP запрос POST /number/ с телом option={Вариант}.
conn = http.client.HTTPConnection("167.172.172.227:8000")
headers = {'Content-type': 'application/x-www-form-urlencoded'}
conn.request('POST', '/number/', 'option=10', headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)

data1 = r1.read().decode()
left = operate(data1, left)
print(left)

#Задание 4: Отправить HTTP запрос PUT /number/ с телом JSON {"option": {Вариант}}.
conn = http.client.HTTPConnection("167.172.172.227:8000")
headers = {'Content-type': 'application/json'}
conn.request('PUT', '/number/', json.dumps({'option': 10}), headers)
r1 = conn.getresponse()

print(r1.status, r1.reason)

data1 = r1.read().decode()
left = operate(data1, left)
print(left)

#Задание 5: Отправить HTTP запрос DELETE /number/ с телом JSON {"option": {Вариант}}.
conn = http.client.HTTPConnection("167.172.172.227:8000")
conn.request('DELETE', '/number/', json.dumps({'option': 10}))
r1 = conn.getresponse()
print(r1.status, r1.reason)

data1 = r1.read().decode()
left = operate(data1, left)
print(left)
