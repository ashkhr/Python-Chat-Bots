from flask import Flask,make_response,render_template, request, jsonify, json,jsonify,redirect,url_for
import re, collections
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from app import db,User_auth
app = Flask(__name__)        

from conversation import getReply
from software_download import getInfo

@app.route('/getAnswer')     
def getAnswer():
    """ Server side end point from user """
    userQuery = request.args.get("query") 
    userDialog = request.args.get("dialog") # handles the user diaog
    intent = request.args.get("intent")
    print (request.environ['REMOTE_ADDR'])
    print (userDialog,userQuery)
    response=''
    if userDialog=='initial':
        if 'last' in userQuery.split() or 'transaction' in userQuery.split() or 'transactions' in userQuery.split():
            intent='last batch'
                
        elif 'problem' in userQuery.split() or 'terminal' in userQuery.split():
            intent='software download'
    
    if intent=='last batch':
        response,userDialog,intent=getReply(userQuery,userDialog,intent)
    elif intent=='software download':
        response,userDialog,intent=getInfo(userQuery,userDialog,intent)
        
    return jsonify(response=response,id="1",status="suc",dialog=userDialog,intent=intent)

@app.route('/agent')     
def agent():
    return render_template('la test firstdata.html')


@app.route('/')
@app.route('/index')
def index():
    #return make_response(send())
    #headers = {'Content-Type': 'text/html'}    
    return make_response(render_template('index.html'),200)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True,debug=True,port=8000)