import re, collections
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import pickle
#import thread
from app import db,User_auth
import time
import requests
import json
from API import Create_Case

        
def getReply(query,dialog,intent):
    speech_output=[]

    
    global usecase
    global session
    global caseno
    global visitor_ack
    global agent_ack
    global chat
    global session_key
    global session_id
    global aff_tok
    global chat
    global Prod
    global qnt
    global f
    
    try:
        
        if dialog=='initial':
            speech_output.append('Ok, I can help you placing an Order')
            speech_output.append('Please provide the Product name')
            dialog='GetProdName'      
        elif dialog=='GetProdName':
             speech_output.append("Please enter Product quantity")
             Prod=query
             dialog='GetProdQnt'
        elif dialog=='GetProdQnt':
             qnt=query
             s=User_auth.query.filter_by(id=1).first()
             cs=Create_Case(s.usernames,s.email,s.category,s.topic,s.areyou,Prod,qnt)
             speech_output.append("Order Placed, Please note the Order No :<b>({})</b> for future reference.".format(cs['CaseNumber']))
             speech_output.append('Please confirm, if would like to buy more product - Yes/No')
             dialog='Moreprod'  
        elif dialog=='Moreprod':
             if query=='yes' or query=='Yes' or query == 'YES':
                 speech_output.append('Enter Product name')
                 dialog='GetProdName' 
             else:
                speech_output.append('Thank you for contacting Allergan Customer Service BOT.')
                dialog='Moreprod' 
        else:
            speech_output.append('Restart....')
            dialog='initial'
    except Exception as e:
        speech_output.append('Server is down. Please try refreshing page and start again.')
        print (dialog)
        print ("Exception: "+str(e))
        return speech_output,dialog,intent
            
    print (dialog)
    return speech_output,dialog,intent


    
