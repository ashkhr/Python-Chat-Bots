from flask import Flask,make_response,render_template, request, jsonify, json,jsonify,redirect,url_for
import re, collections
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
from app import app, db,User_auth        
db.init_app(app)
from conversation import getReply


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
        intent='customer_query'
    
    if intent=='customer_query':
        response,userDialog,intent=getReply(userQuery,userDialog,intent)
    else:
        pass
    return jsonify(response=response,id="1",status="suc",dialog=userDialog,intent=intent)

@app.route('/')
@app.route('/index')
def index():

    #return make_response(send())
    #headers = {'Content-Type': 'text/html'}    
    return make_response(render_template('start.html'),200)

@app.route('/chatbot',methods=['GET','POST'])
def chatbot():
    name=''
    if request.method=='POST':
        s=User_auth.query.filter_by(id=1).first()
        if s:
            print ('deleted')
            db.session.delete(s)
            db.session.commit()

        form=request.form
        name=form['name']
        email=form['email']
        category=form['sel1']
        topic = form['sel2']
        areyou = form['sel3']
        db.session.add(User_auth(usernames=name,email=email,category=category,topic=topic,areyou=areyou,tracking_number=''))
        db.session.commit()
        print (name,email,category,topic,areyou)
    else:
        s=User_auth.query.filter_by(id=1).first()
        name=s.usernames



    


    return make_response(render_template('index.html',name=name),200)

    
if __name__ == '__main__':
    app.run(host='0.0.0.0',threaded=True,debug=True,port=8002)