import requests
import json

def get_session_id():
    try:
        url="https://login.salesforce.com/services/Soap/u/35.0"
        #headers = {'content-type': 'application/soap+xml'}
        headers = {'content-type': 'text/xml','soapaction':'login'}  
        body = """<?xml version="1.0" encoding="utf-8" ?>
                  <env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
                   <env:Body>
                       <n1:login xmlns:n1="urn:partner.soap.sforce.com">
                           <n1:username>akhiljoy.kandamkulathy@cognizant.com.fdbotdemo</n1:username>
                           <n1:password>innovate@123</n1:password>
                       </n1:login>
                   </env:Body>
                 </env:Envelope>"""
        response = requests.post(url,data=body,headers=headers)

        from xml.etree.ElementTree import XML
        data = XML(response.text)   
        session=''
        for i in data.iter():
            s=i.tag
            if 'sessionId' in s.split('}'):
                print (i.text)
                session=i.text
        return session        
        
    except Exception as exc:
        return exc
           
def create_case(Name, email, IssueType, IssueSubType, Areyou , TrackingNo):
    try:
        session = get_session_id()
        print("Session :" + session)
        url='https://fdbotdemo.my.salesforce.com/services/apexrest/UPSRestServiceCreateCase'
        payload = {
                    "Name": Name,
                    "email": email,
                    "SupportCategory": IssueType,
                    "SupportTopic": IssueSubType,
                    "Areyou": Areyou,
                    "TrackingNo": TrackingNo
                  }
       
        headers = {'Content-type': 'application/json','Authorization': 'Bearer '+session}
       
        r = requests.post(url, json=payload, headers=headers)
        print (payload)   
        val=r.json()
        return val
            
    except Exception as exc:
        return exc
           
c=create_case('James Collins','james@outlook.com','Tracking a Package','Tracking Information','Receiver','1Z 999 AA1 01 2345 6784')
print(c)
#dialog='Case:5002800000idVz9AAE:kA028000000JZWyCAO:00001059' 
#print(dialog)
#print('Case Id ' + dialog[5:23])
#print('Article Number ' + dialog[24:42])
#print('Case Number ' + dialog[43:51])

#a= close_case('5002800000idWJTAA2','kA028000000JZWyCAO')  
#print(a['caseno'])
#print(a['artno'])

   