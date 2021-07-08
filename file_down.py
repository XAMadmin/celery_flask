# coding:utf-8
import  json
 
from  flask  import  Flask, make_response
 
app  =  Flask(__name__)
 

# 利用python web框架做文件流下载 
@app .route( '/download' , methods = [ "GET" ])
def  download():
   user  =  { 'name' :  'dewei' ,  'age' :  33 }
 
   data  =  json.dumps(user)
   response  =  make_response(data)
   response.headers[ 'content-type' ]  =  'application/octet-stream;charset=utf-8'
   response.headers[ 'content-disposition' ]  =  'attachment;filename=user.json'
   return  response
 
if  __name__  ==  '__main__' :
   app.run(host = '0.0.0.0' , port = 5005 , debug = True )