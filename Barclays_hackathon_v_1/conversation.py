import re, collections
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper
import pickle
import thread
from app import db,User_auth
import time

import requests
import json

        
def getReply(query,dialog,intent):
    speech_output=[]
    
    mastercard=''
    bitcoin_u1=''
    visa_u1=''
    vouchers_u1=''
    
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
    global f
    
    try:
        if dialog=='live agent active':
            print ('here')
            


            s=User_auth.query.filter_by(id=1).first()

            url = 'https://d.la3-c1-dfw.salesforceliveagent.com/chat/rest/System/SessionId'
            payload = {}
            #headers = {'Authorization': 'Bearer 00D6F000000FiLV!AQsAQIwC_AS38aalSQzWK0SuJJuBMslH1SO0dWtaC.B_SDwqwA6..CqxpKYnYZqz4ndMuvbQquTsCR2s90Zm5IUdaO0v6oEw'}
            headers = {'X-LIVEAGENT-API-VERSION': '38','X-LIVEAGENT-AFFINITY': 'null','Content-Type':'application/json'}
            
            #r = requests.post(url, data=json.dumps(payload), headers=headers)
            r = requests.get(url,params=payload,headers=headers)
            print (r)
            
            val=r.json()
            session_key=val['key']
            session_id=val['id']
            aff_tok=val['affinityToken']
            
            
            #**********************************************************************************************#
            print ('*********************************************************************')
            
            url = 'https://d.la3-c1-dfw.salesforceliveagent.com/chat/rest/Chasitor/ChasitorInit'
            payload = {"organizationId": '00D46000000Z9aY',
                "deploymentId": '57246000000fzmx',
                "buttonId": '57346000000g008',
                "sessionId": session_id,
                "doFallback": 'true',
                "userAgent": "",
                "language": "en-US",
                "screenResolution": "1920x1080",
                "visitorName": s.usernames,
                "prechatDetails": [],
                "prechatEntities": [],
                "receiveQueueUpdates": True,
                "isPost": True
                }
            #headers = {'Authorization': 'Bearer 00D6F000000FiLV!AQsAQIwC_AS38aalSQzWK0SuJJuBMslH1SO0dWtaC.B_SDwqwA6..CqxpKYnYZqz4ndMuvbQquTsCR2s90Zm5IUdaO0v6oEw'}
            headers = {'X-LIVEAGENT-API-VERSION': '38','X-LIVEAGENT-AFFINITY': aff_tok,'X-LIVEAGENT-SESSION-KEY':session_key,'Content-Type':'application/json'}
            
            #r = requests.post(url, data=json.dumps(payload), headers=headers)
            r = requests.post(url,json=payload,headers=headers)
            print (r)
            
            
            #**********************************************************************************************#
            print ('*********************************************************************')
            
            url = 'https://d.la3-c1-dfw.salesforceliveagent.com/chat/rest/Chasitor/ChatMessage'
            payload = {
            'text':chat
            }
            visitor_ack+=1
            
            headers = {'X-LIVEAGENT-API-VERSION': '38','X-LIVEAGENT-AFFINITY': aff_tok,'X-LIVEAGENT-SEQUENCE':str(visitor_ack),'X-LIVEAGENT-SESSION-KEY':session_key,'Content-Type':'application/json'}
            
            #r = requests.post(url, data=json.dumps(payload), headers=headers)
            r = requests.post(url,json=payload,headers=headers)
            print (r)
            
            #**********************************************************************************************#
            print ('*********************************************************************')
            
            flag=True
            url = 'https://d.la3-c1-dfw.salesforceliveagent.com/chat/rest/System/Messages'
            agent_ack=1
            while(flag):
            
                payload = {'ack':str(agent_ack)}
                #headers = {'Authorization': 'Bearer 00D6F000000FiLV!AQsAQIwC_AS38aalSQzWK0SuJJuBMslH1SO0dWtaC.B_SDwqwA6..CqxpKYnYZqz4ndMuvbQquTsCR2s90Zm5IUdaO0v6oEw'}
                headers = {'X-LIVEAGENT-API-VERSION': '38','X-LIVEAGENT-AFFINITY': aff_tok,'X-LIVEAGENT-SEQUENCE':str(agent_ack),'X-LIVEAGENT-SESSION-KEY':session_key,'Content-Type':'application/json'}
                
                #r = requests.post(url, data=json.dumps(payload), headers=headers)
                r = requests.get(url,params=payload,headers=headers)
                print (r)
                
                print (r.text)
                
                if r.status_code!=204:
                    val=r.json()
                    agent_ack=val['sequence']
                    for i in range(0,len(val['messages'])):
                    
                        if val['messages'][i]['type']=='ChatMessage':
                            print (val['messages'][i]['message']['text'])
                            speech_output.append(val['messages'][i]['message']['text'])
                            flag=False
                            break
                else:
                    pass
                    
            time.sleep(5)    
            
            dialog='live agent active2'
            
        elif dialog=='live agent active2':
            
            
            visitor_ack+=1
            url = 'https://d.la3-c1-dfw.salesforceliveagent.com/chat/rest/Chasitor/ChatMessage'
            payload = {
            'text':query
            }
        
            headers = {'X-LIVEAGENT-API-VERSION': '38','X-LIVEAGENT-AFFINITY': aff_tok,'X-LIVEAGENT-SEQUENCE':str(visitor_ack),'X-LIVEAGENT-SESSION-KEY':session_key,'Content-Type':'application/json'}
            
            
            r = requests.post(url,json=payload,headers=headers)
            print (r)
            
            flag=True
            url = 'https://d.la3-c1-dfw.salesforceliveagent.com/chat/rest/System/Messages'
            while(flag): 
                payload = {
                    'ack':str(agent_ack)
                }
                #headers = {'Authorization': 'Bearer 00D6F000000FiLV!AQsAQIwC_AS38aalSQzWK0SuJJuBMslH1SO0dWtaC.B_SDwqwA6..CqxpKYnYZqz4ndMuvbQquTsCR2s90Zm5IUdaO0v6oEw'}
                headers = {'X-LIVEAGENT-API-VERSION': '38','X-LIVEAGENT-AFFINITY': aff_tok,'X-LIVEAGENT-SEQUENCE':str(agent_ack),'X-LIVEAGENT-SESSION-KEY':session_key,'Content-Type':'application/json'}
                
                #r = requests.post(url, data=json.dumps(payload), headers=headers)
                r = requests.get(url,params=payload,headers=headers)
                print (r)
                print (r.text)
                
                if r.status_code!=204:
                    val=r.json()
                    agent_ack=val['sequence']
                    for i in range(0,len(val['messages'])):
                        if val['messages'][i]['type']=='ChatMessage':
                            print (val['messages'][i]['message']['text'])
                            speech_output.append(val['messages'][i]['message']['text'])
                            flag=False
                        
                        if val['messages'][i]['type']=='ChatEnded':
                            url='https://fdbotdemo.my.salesforce.com/services/apexrest/v1/FDBDRestServiceCaseOperations'
                            flag=False
                            dialog='initial'
                            intent=''
                            speech_output.append('Chat Ended')
                            break
                        
                        if flag==False:
                            break   
                else:
                    pass
                
                    
                    
                    
                time.sleep(5)
        
        
        elif dialog=='initial':
            chat=''
            chat+='Customer>> '+query
            speech_output.append('Let me take a look. Can you please help me with the Tracking Number OR InfoNotice Number?')
            dialog='mid'
            chat+='\n Chatbot>> '+speech_output[0] +'\n'
        
        elif dialog=='mid':
            chat+='Customer>> '+query
            s=User_auth.query.filter_by(id=1).first()
            s.tracking_number=query
            db.session.commit()
            speech_output.append('Thanks, our records indicate that the package has been delivered to your friend.')
            speech_output.append("We're sorry that he hasn't been able to locate your package. Please ask him to check with other members of his household or delivery address.")
            speech_output.append('For residences, check around porches, back doors, and with any close neighbors.')
            dialog='mid-new'
            chat+='\n Chatbot>> '+ ' '.join(speech_output[0:len(speech_output)-1]) +'\n'
        
        
        elif dialog=='mid-new':
            chat+='Customer>> '+query
            speech_output.append('Sure.')
            speech_output.append('Would you like me to create a request straight away, or would you prefer to chat with one of our customer care representatives?')
            dialog='ask-for-agent2'
            chat+='\n Chatbot>> '+' '.join(speech_output[0:len(speech_output)-1]) +'\n'
            
        elif dialog=='ask-for-agent2':
            chat+='Customer>> '+query
            
            if 'case' in query.lower().split() or 'create' in query.lower().split():
                from CreateCaseAPI_New import create_case
                s=User_auth.query.filter_by(id=1).first()
                c=create_case(s.usernames,s.email,s.category,s.topic,s.areyou,s.tracking_number)
                print(c)
                dialog='initial'
                intent=''
                speech_output.append('Thanks for the confirmation.')
                speech_output.append(" I have logged a complaint with your concerns and passed it on to our customer care representatives to investigate on priority.")
                speech_output.append('Please note down the Complaint # <b>({})</b> for future reference related to this complaint.'.format(c['CaseNumber']))
            else:
                visitor_ack=0
                speech_output.append('Thanks for the confirmation. I will transfer you to one of our Customer Care Representative.')
                
                dialog='live agent'
            
            chat+='\n Chatbot>> '+speech_output[0] +'\n' + 'End'        
    
    except Exception as e:
        speech_output.append('Server is down. Please try refreshing page and start again.')
        print (dialog)
        print ("Exception: "+str(e))
        return speech_output,dialog,intent
            
    print (dialog)
    return speech_output,dialog,intent