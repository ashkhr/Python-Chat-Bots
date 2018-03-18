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
from API import Create_Case,Find_Product,Find_Account,Add_Product

        
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
    global ProdName
    global shipAcc
    global qnt
    global f
    global more
    global CaseNum
    
    try:
        
        if dialog=='initial':
             speech_output.append('Ok, I can help you placing an Order')
             speech_output.append("Please provide the Product name")
             #speech_output.append('Please provide the ship to account name')
             dialog='GetProdName'                   
        elif dialog=='GetProdName':
             speech_output.append("Please provide the Product Unit/Vials - 100 / 200 / 300")
             Prod=query
             p1=Find_Product(Prod)
             dialog='GetProdUnit'
        elif dialog=='GetProdUnit':
             Prod=Prod +' '+query
             p1=Find_Product(Prod)
             if p1['response']=='Product found':
                 speech_output.append("Please provide the Product quantity")
                 ProdName=p1['prodName']
                 dialog='GetPrdQty'
             else:
                 speech_output.append('Entered product does not exist in Product catlog. Please provide valid Product name with units')
                 speech_output.append('Please provide the Product name')
                 dialog='GetProdName'  
                 
        elif dialog=='GetPrdQty':
             qnt=query
             speech_output.append("Is the shipping account different - Yes/No")
             dialog='ConfirmShipAcc'
             
        elif dialog=='ConfirmShipAcc':
             if  "Yes" in query or  "yes" in query:
                speech_output.append("Please provide the ship to account name")  
                dialog='GetAccName'
             elif "No" in query or  "no" in query:
                s=User_auth.query.filter_by(id=1).first()
                shipAcc = s.email
                speech_output.append('Please validate Product details.')
                speech_output.append("Product Name : <b>{}</b> ".format(ProdName))
                speech_output.append("Quantity : <b>{}</b> ".format(qnt))
                speech_output.append("Shipping account  : <b>{}</b> ".format(shipAcc))
                speech_output.append('Are all the product details corect, Please confirm so that I can place an Order - Yes/No')
                dialog='Conformed'
             else:
                speech_output.append('Sorry, I did not understand it, Can you please enter the valid input')
                speech_output.append("Is the shipping account different - Yes/No")
                dialog='ConfirmShipAcc'              
            
        elif dialog=='GetAccName':
             accName=query
             a1=Find_Account(accName,'Find')
             if a1['response']=='Account found':
                 shipAcc=a1['accName']
                 speech_output.append('Please validate Product details.')
                 speech_output.append("Product Name : <b>{}</b> ".format(ProdName))
                 speech_output.append("Quantity : <b>{}</b> ".format(qnt))
                 speech_output.append("Shipping account  : <b>{}</b> ".format(shipAcc))
                 speech_output.append('Are all the product details corect, Please confirm so that I can place an Order - Yes/No')
                 dialog='Conformed'
             else:
                 speech_output.append('Entered Account does not exist.Please provide valid Account name')
                 speech_output.append('Please provide the ship to account name')
                 dialog='GetAccName'
                            
        elif dialog=='Conformed':
            if  "Yes" in query or  "yes" in query:
                s=User_auth.query.filter_by(id=1).first()
                c=Create_Case(s.usernames,s.email,shipAcc,s.topic,s.areyou)
                CaseNum=c['CaseNumber']
                #print(c['response'])
                #speech_output.append('Creating Case')
                #speech_output.append('Adding Product')
                p=Add_Product(CaseNum,ProdName,qnt)
                #print(p['response'])
                speech_output.append('Please confirm, if you would like to order more product - Yes/No')
                dialog='Moreprod'
            elif "No" in query or  "no" in query:
                speech_output.append('Please provide the Product details again')
                speech_output.append('Please provide the Product name')
                dialog='GetProdName'
            else:
                speech_output.append('Sorry, I did not understand it, Can you please enter the valid input')
                speech_output.append('Are all the product details corect, Please confirm so that I can place an Order - Yes/No')
                dialog='Conformed'
              
        elif dialog=='Moreprod':
             if  "Yes" in query or  "yes" in query:
                 speech_output.append('Please provide the Product name')
                 dialog='GetProdName1' 
             else:
                speech_output.append ("Order Placed, Please note the Order No : <b>{}</b> for future reference.".format(CaseNum))
                speech_output.append(' Is there anything else that I can help you with? - Yes/No')
                dialog='end'
                
        elif dialog=='end':
                speech_output.append('Thank you for contacting Allergan Customer Service BOT.')
                dialog='Botend'
        
        elif dialog=='GetProdName1':
             speech_output.append("Please provide the Product Unit/Vials - 100 / 200 / 300")
             Prod=query
             p1=Find_Product(Prod)
             dialog='GetProdUnit1'
        elif dialog=='GetProdUnit1':
             Prod=Prod +' '+query
             p1=Find_Product(Prod)
             if p1['response']=='Product found':
                 speech_output.append("Please provide the Product quantity")
                 ProdName=p1['prodName']
                 dialog='ConformProduct1'
             else:
                 speech_output.append('Entered product does not exist in product catlog.Please provide valid Product name with units')
                 speech_output.append('Please provide the Product name')
                 dialog='GetProdName1'  
            
        elif dialog=='ConformProduct1':
             qnt=query
             speech_output.append('Please validate Product details.')
             speech_output.append("Product Name is :<b>{}</b> ".format(ProdName))
             speech_output.append("Quantity is :<b>{}</b> ".format(qnt))
             speech_output.append('Are all the product details corect, Please confirm so that I can place an Order - Yes/No')
             dialog='Conformed1'
             
        elif dialog=='Conformed1':
            if  "Yes" in query or  "yes" in query:
                p=Add_Product(CaseNum,ProdName,qnt)
                #print(p['response'])
                #Add product 
                #speech_output.append('Adding Product')
                speech_output.append('Please confirm, if you would like to order more product - Yes/No')
                dialog='Moreprod'
            elif "No" in query or  "no" in query:
                speech_output.append('Please provide Product details again')
                speech_output.append('Provide the Product name')
                dialog='GetProdName1'  
            else:
                speech_output.append('Unable to understand what you are trying to say..Can you please repeate')
                
                
        else:
            speech_output.append('Unable to understand what you are trying to say..Can you please repeate')
            dialog='initial'
    except Exception as e:
        speech_output.append('Server is down. Please try refreshing page and start again.')
        print (dialog)
        print ("Exception: "+str(e))
        return speech_output,dialog,intent
            
    print (dialog)
    return speech_output,dialog,intent