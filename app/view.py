### imports

from flask import Flask, render_template, request, abort, jsonify, Response, url_for
from requests import get
import sys, codecs
from dlx import DB, Bib, Auth
import structure
import header
import re
import time 
import os
from config import CONSTRING

### setting up the parameters

URL_BY_DEFAULT='https://9inpseo1ah.execute-api.us-east-1.amazonaws.com/prod/symbol/'
DB.connect(CONSTRING)
body = ""
session = ""
bodsess=""
APP_ROOT= os.path.dirname(os.path.abspath(__file__))


# Initialize your application

app = Flask(__name__)


########################################################################################################
########################  STEP 01 : Extract DATA #######################################################
########################################################################################################


### Some variables
auth_ids = {}
myBib=[]
myAuth=[]
myfinalBib=[]  
agenda=[]
record=[]
value={}
cursor=[]
list_agenda_title=set()
dict_itp_online={}
list_itp_online=[]

### find the bibs for the session, print them in marc21, and save any found xrefs.

def processITP(body,session):

     

    cursor = Bib.match_fields_or (
        ('191', ('b', body), ('c', session)),
        ('791', ('b', body), ('c', session))
    )

    ### get the global bibs records 

    print("please wait the system is processing bibs records...")

    for bib in cursor:
        for xref in bib.get_xrefs():
            auth_ids[xref] = True
        myBib.append(bib)

    ### get the final bib records from the global bib records
    ## TO DO  991$z  = I and the 930$a starts with UND 


    for bib in myBib:
        recup="".join(str(e) for e in bib.get_values('930','a'))
        recup1="I"
        if ((recup1 in bib.get_values('991','z')) and (recup.startswith("UND"))):
            myfinalBib.append(bib)


    ### get the global auths records

    print("please wait the system is processing auths records...")

    for auth_id in sorted(auth_ids.keys()):
        auth = Auth.match_id(auth_id)
        myAuth.append(auth)

    ### get the agendas records from the global auth records (filter with 191$a)


    for auth in myAuth:
        recup="".join(str(e) for e in auth.get_values('191','a'))
        if recup==bodsess:
            agenda.append(auth)


    ### writing a file with the bib record information
    #with open(myPath, 'w+') as out:
    # loading myfinalBib variable
    #    for bib in myfinalBib:
    #        //


########################################################################################################
########################  STEP 02 : PROCESSING   #######################################################
########################################################################################################

# init the values

def initValue():
    count=0
    value.clear()
    auth_ids.clear()
    myBib.clear()
    myAuth.clear()
    myfinalBib.clear() 
    agenda.clear()
    record.clear()
    cursor.clear()
    list_agenda_title.clear()
    list_itp_online.clear()
    dict_itp_online.clear()
    
    

### get the header from the haeder list using the code and the body

def getHeader(myList):

    recup=set()   
    for ml in myList:    

        if ml[0]=='X':
            recup.add(header.headerS[ml.strip()])

        if ml[0]=='T':
            recup.add(header.headerT[ml.strip()])

        if ml[0]=='C':
            recup.add(header.headerE[ml.strip()])

        if ml[0]=='G':
            recup.add(header.headerA[ml.strip()])

        if ml[0] not in ['C','T','G','X'] :
            recup.add("Not Header implemented!!!")

    return list(recup)

def getLink(myList,myUrl):
    recup=[]    
    for ml in myList:
        recup.append(myUrl+ml)
    return recup

########################################################################################################
########################  STEP 02 : PROCESSING   #######################################################
########################################################################################################

# Querying and displaying the results
@app.route("/")
@app.route("/fullcontent",methods=['POST','GET'])

def fullcontent():
    
    if request.method == 'POST':

        # Retrieve the paramaters of the search
        initValue()        
        myBody,mySession=request.form["body"],request.form["session"]
        
        # Start the counter
        startTime=time.time()
        

        # creation of the folder on disk and upload the file selected
        target=os.path.join(APP_ROOT,"files")
        
        if not os.path.isdir(target):
            os.mkdir(target)

        # Check the existence of the file containing values in the disk
        bodsess=myBody+mySession
        #fileSession=myBody[0]+mySession+".txt"  
        #print(fileSession) 
        
        #fullPath='{}/{}'.format(target,fileSession)
        #print(fullPath)
        #exists = os.path.isfile(fullPath)
        #print(exists)
        #if exists:
            # Opening the file
        #    with open(fullPath, 'r') as out:
            # loading myfinalBib variable
        #        mesData=list(out)
        #        for data in  mesData: 
        #            myfinalBib.append()

        #else :
            # Extract the records
        #    processITP(myBody,mySession,fullPath)

        processITP(myBody,mySession)

        # Load the agenda titles values
        for bib in myfinalBib:
            values=",".join(bib.get_values("991","d")).split(",")
            for value in values:
                list_agenda_title.add(value)

        record=sorted(list(list_agenda_title))

        # Load the other itp_online values
        for bib in myfinalBib:
            values=",".join(bib.get_values("991","d")).split(",")
            for rec in record:
                if rec in values:
                    dict_itp_online["subject"]=rec
                    dict_itp_online["heading"]=getHeader(bib.get_values("191","9"))
                    dict_itp_online["docsymbol"]=bib.get_values("191","a")
                    dict_itp_online["link"]=getLink(bib.get_values("191","a"),URL_BY_DEFAULT)
                    list_itp_online.append(dict_itp_online.copy())
                    dict_itp_online.clear()

        # Stop the counter
        endTime=time.time()

        # Return the values generated
        return(render_template('fullcontent.html',record=list_itp_online,count=len(list_itp_online),myTime=round(endTime-startTime)))

    if request.method == 'GET':
        return(render_template('fullcontent.html'))
