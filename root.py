from ast import Delete
import firebase_admin
from firebase_admin import db, credentials
import json
from twilio.rest import Client 

cred = credentials.Certificate('schannel-538d4-firebase-adminsdk-fp41y-f2a6a4646d.json')

firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://schannel-538d4-default-rtdb.firebaseio.com/'	
})

ref = db.reference('SChannel')
channels = ref.child('Channels')
channelgroups = ref.child('ChannelGroups')
workflow = ref.child('Workflows')

channelName = ref.child("Tables").child("Channels").child("Name").get()
channelEmail = ref.child("Tables").child("Channels").child("Email").get()
channelPhone = ref.child("Tables").child("Channels").child("Phone Number").get()
channelItems = ref.child("Tables").child("Channels").child("Items Bought").get()

channelGroupID = ref.child("Tables").child("Channel Groups").child("GroupID").get()
channelGroupEmail = ref.child("Tables").child("Channel Groups").child("Email Addresses").get()
channelGroupWhatsapp = ref.child("Tables").child("Channel Groups").child("Whatsapp Numbers").get()
channelGroupSMS = ref.child("Tables").child("Channel Groups").child("SMS Numbers").get()

workflowID = ref.child("Tables").child("Workflow").child("ID").get()
workflowEmailTemp = ref.child("Tables").child("Workflow").child("Email template").get()
workflowWhatsappTemp = ref.child("Tables").child("Workflow").child("Whatsapp template").get()
workflowSMSTemp = ref.child("Tables").child("Workflow").child("SMS template").get()

#print(ref.child('Tables').get())
#handle = db.reference('SChannel/Tables')

account_sid = 'AC91c5afebf10d075eb56a120c957845ee' 
auth_token = '6b6b5ed94e20a62803d7d704952c996a'
client = Client(account_sid, auth_token) 

def sendWAmessage(WAbody, WAnumber):
    WAmessage = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body=WAbody,      
                              to=('whatsapp:+1' + WAnumber) 
                          ) 
    print(WAmessage.sid)

def sendSMSmessage(SMSbody, SMSnumber):
    SMSmessage = client.messages.create(  
                              messaging_service_sid='MGf5e2fc1adb92c28055b10b7662293d00', 
                              body=SMSbody,      
                              to=('+1' + SMSnumber) 
                          ) 
    

#sendWAmessage(workflowWhatsappTemp, channelGroupWhatsapp)
#sendSMSmessage(workflowSMSTemp, channelGroupSMS)