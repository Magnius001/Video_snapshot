import requests

url= 'http://localhost:9999'

payload={'fplate': '51G12345', 'bplate': '51G67890', 'c1': 'ABCD123456', 'c2': 'NA'}

headers={"Action": "Shot"}

r=requests.post(url,headers=headers,json=payload)

print(r.content)