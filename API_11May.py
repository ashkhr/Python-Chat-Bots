import requests
import json

def get_session_id():
    try:
        url="https://test.salesforce.com/services/Soap/u/35.0"
        #headers = {'content-type': 'application/soap+xml'}
        headers = {'content-type': 'text/xml','soapaction':'login'}  
        body = """<?xml version="1.0" encoding="utf-8" ?>
                  <env:Envelope xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xmlns:env="http://schemas.xmlsoap.org/soap/envelope/">
                   <env:Body>
                       <n1:login xmlns:n1="urn:partner.soap.sforce.com">
                           <n1:username>aiPOC@allergan.com.aipoc</n1:username>
                           <n1:password>welcome321</n1:password>
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

def Create_Case(ContactName,AccountName,ShipToAccName,BusinessUnit,SalesRep,ProductName,Quantity):
    try:
        session = get_session_id()
        print("Session :" + session)
        url='https://cs85.salesforce.com/services/apexrest/RestServiceCreateCase'
        payload = {
                "ContactName":ContactName,
                "AccountName":AccountName,
                "ShipToAccName":ShipToAccName,
                "BusinessUnit":BusinessUnit,
                "SalesRep":SalesRep,
                "ProductName":ProductName,
                "Quantity":Quantity
                 }
       
        headers = {'Content-type': 'application/json','Authorization': 'Bearer '+session}
       
        r = requests.post(url, json=payload, headers=headers)
        print (payload)   
        val=r.json()
        return val
            
    except Exception as exc:
        return exc
    

    
#s= get_session_id()
#print(s)
#s = Update_Account_Email('CENTRO ESPECIALIZADO EM OFTALMOLOGI','test@sample.com')   
#print(s['responseMessage'])
a=Create_Case('MARA KATE','Horward MBA','Agnieszka Zielinska','Ophthalmology','Agnieszka Zielinska','ProductName','Quantity')
print(a['CaseNumber'])
