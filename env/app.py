#Imports
from random import randint
import firebase_admin
import pyrebase
import json
from uuid import uuid4
from firebase_admin import credentials, auth, db
from flask import Flask, request, render_template, redirect, url_for
from forms import CreateUserForm, DeleteUserForm, AddUserForm, RemoveUserForm, CreateGroup , EditGroup, SendMessage
from functools import wraps
from twilio.rest import Client
import collections
from collections.abc import MutableMapping

#App configuration
app = Flask(__name__)

app.config['SECRET_KEY'] = '166bd6c8c805a8a3a4e62b55f36219a737f0345dba389cce'

#Connect to firebase
cred = credentials.Certificate('schannel-538d4-firebase-adminsdk-fp41y-f2a6a4646d.json')
firebase = firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://schannel-538d4-default-rtdb.firebaseio.com/'	
})
pb = pyrebase.initialize_app(json.load(open('sChannelconfig.json')))


#Initialize messaging information
account_sid = 'AC91c5afebf10d075eb56a120c957845ee' 
auth_token = '6b6b5ed94e20a62803d7d704952c996a'
client = Client(account_sid, auth_token) 

#Creating variables from DB
ref = db.reference('SChannel')
channels = ref.child('Channels')
channelgroups = ref.child('ChannelGroups')
workflow = ref.child('Workflows')
tables = ref.child('Tables')

channelsCount=0
channelGroupCount=0
workflowCount=0

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

#Additional test data source
users = [{'uid': 1, 'name': 'Steven Yeun'}]

#Code to check that 
def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap

#Api route to get users
@app.route('/api/userinfo')
@check_token
def userinfo():
    return {'data': users}, 200

#Api route to sign up a new user
@app.route('/api/signup')
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'},400
    try:
        user = auth.create_user(
               email=email,
               password=password
        )
        return {'message': f'Successfully created user {user.uid}'},200
    except:
        return {'message': 'Error creating user'},400

#Api route to get a new token for a valid user
@app.route('/api/token')
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except:
        return {'message': 'There was an error logging in'},400

#Api route to admin home 
@app.route('/', methods=['GET', 'POST'])
def admin():
    global channelsCount #obj to generate user IDs - there is probably a much better way of doing this, channelsCount+=1 is a placeholder
    channelsCount+=1
    createuser_form = CreateUserForm()
    deleteuser_form = DeleteUserForm()
    if createuser_form.submit() :
        channels.child(str(channelsCount)).set({ #find alternative to channelsCount 
            'First Name' : createuser_form.first_name.data, 
            'Last Name' : createuser_form.last_name.data, 
            'Email' : createuser_form.email.data, 
            'Phone Number' : createuser_form.phone_number.data, 
            "User ID" : str(channelsCount)
            })
    #if deleteuser_form.submit() : 
        #the idea was to query 
    return render_template('admin.html', createuser_form=createuser_form, 
    deleteuser_form=deleteuser_form)

#Api route to creating a new group
@app.route('/api/editgroup', methods=['GET', 'POST']) # want to change address to '/api/<groupid>' somehow
def editgroup():
    groups = channelgroups.get()
    adduser_form = AddUserForm() #modify to add user to a group - ie add a key/value that connects to group id in question
    removeuser_form = RemoveUserForm() #modify to remove user from a group (either set key value to null or delete child altogether)
    editgroup_form = EditGroup()
    sendmessage_form = SendMessage()
    #set the user indicated by adduser_form and modify channelgroup key to add cgID, true
    #delete channel group ID from user indicated by removeuser_form.first_name/last_name.data
    #if editgroup_form.submit:
    #    channelgroups.child(INSERT PARTICULAR GROUP ID HERE).set({
    #        'Group Name' : editgroup_form.group_name.data, 
    #        'Group Description' : editgroup_form.group_desc.data
    #        })
    #for user in groups
    #def sendSMSmessage(sendmessage_form.message_body, channelPhone): #take channelPhone and pass to channelphone in for loop
    #    SMSmessage = client.messages.create(  
    #        messaging_service_sid='MGf5e2fc1adb92c28055b10b7662293d00', 
    #        body=sendmessage_form.message_body,      
    #        to=('+1' + channelPhone)) 
    return render_template('editgroup.html', adduser_form=adduser_form, 
        removeuser_form=removeuser_form, groups=groups, editgroup_form=editgroup_form,
        sendmessage_form=sendmessage_form)

@app.route('/api/groupgrid', methods=['GET', 'POST'])
def groupgrid():
    creategroup_form = CreateGroup()
    global channelGroupCount
    channelGroupCount+=1
    groups = channelgroups.get()
    grouplist_name = []
    grouplist_desc = []
    grouplist_ID = []
    print(groups)
    if request.method == 'GET':
        return render_template('groupgrid.html', groups=groups, grouplist_name=grouplist_name, 
        grouplist_desc=grouplist_desc, grouplist_ID=grouplist_ID, creategroup_form=creategroup_form)
    else:
        #creategroup_form.submit():
        channelgroups.child(str(channelGroupCount)).set({
                'Group Name' : creategroup_form.group_name.data, 
                'Group Description' : creategroup_form.group_desc.data, 
                'Group ID' : str(channelGroupCount)
            })
    return render_template('groupgrid.html', groups=groups, grouplist_name=grouplist_name, 
        grouplist_desc=grouplist_desc, grouplist_ID=grouplist_ID, creategroup_form=creategroup_form)

if __name__ == '__main__':
    app.run(debug=True)