import  urllib.request 
import urllib.parse 
import  http.cookiejar 
#post的内容 
values={ 
'u':'16120290', 
'p':'********' 
} 

#登陆的地址 
logUrl="https://gsdb.bjtu.edu.cn/client/login/" 

#构建cook 
cook=http.cookiejar.CookieJar() 

#构建openner 
openner=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cook)) 

#添加headers 
openner.addheaders = [(
	'User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')] 

r=openner.open(logUrl,urllib.parse.urlencode(values).encode()) 

#print(r.read().decode('gbk')) 

r=openner.open("https://gsdb.bjtu.edu.cn/score/info/") 
print('登陆成功!')
with open('123.txt','wb') as f:
	f.write(r.read())
print(r.read().decode())
f.close()