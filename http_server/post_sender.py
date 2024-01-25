import requests

url= 'http://localhost:9999'

payload={'htno': '001111441', 'ecode': 'kuBA2_Supply_Dec_2013'}

headers={"User-Agent": "Some Cool Thing"}

r=requests.post(url,headers=headers,json=payload)

print(r.content)