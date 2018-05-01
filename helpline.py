import imaplib,time,string
import pymysql
import divZone
import pandas as pd
import numpy as np
import data_helper
import divZone
from sklearn.externals import joblib
import tweepy
import time
import pymysql,sys
import statictrain
import webbrowser
clf = joblib.load('svm_tweet.pkl') 
db = pymysql.connect(host,user,password,database)
cursor = db.cursor()

T=time.time()
M = imaplib.IMAP4_SSL('imap.outlook.com',993)
user = your_mail_id
password = mail_password
M.login(user, password)
M.list()
d = {}
id = 12354678
while(1):
    M.select("inbox")
    result, data = M.uid('search', None, "ALL") 
    latest_email_uid = data[0].split()[-1]
    result, data = M.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1]
    M.close()

    import email
    email_message = email.message_from_string(raw_email.decode('utf-8'))
    dat = email_message['Date']
    s=email_message['Subject']
    s=s.split("/")
    if(dat not in d.keys()):
        id = id+1
        d.update({dat : 1})
        s=email_message['Subject']
        s=s.split("/")
        if(s[0]=='H-complaint'):
            text = s[1][14:]
            mobile = s[1][3:13]
            pnr = data_helper.extract_pnr(text)
            tn = data_helper.extract_tn(text)
            if(pnr!=None ):
                flag, division, zone = divZone.division_zone_classifier(pnr)
                if(flag==1):
                    continue
                dept = clf.predict({text})
                sql = """INSERT INTO comp(compid,
                   source,user,complaint,zone,division,department,status)
                   VALUES ('"""+repr(id)+"""', 'SMS', '"""+''+"""', '"""+text+"""','"""+zone+"""','"""+division+"""','"""+dept[0]+"""','')"""
                cursor.execute(sql)
                db.commit()
                db.close()
                url='https://login.bulksmsgateway.in/sendmessage.php?user=username&password=password&mobile=number&message='+mobile+'&message='+repr(id)+" "+" Your Complaint is been forwarded to "+dept[0]+" and to the corresponding division "+division+'&sender=JANMTR&type=3'
                import webbrowser
                webbrowser.open(url)
            elif(tn!=None):
                division, zone = statictrain.stat(tn)
                dept = clf.predict({text})
                if(division ==''):
                    print("Invalid train number")
                sql = """INSERT INTO comp(compid,
                   source,user,complaint,zone,division,department,status)
                   VALUES ('"""+repr(id)+"""', 'SMS', '"""+''+"""', '"""+text+"""','"""+zone+"""','"""+division+"""','"""+dept[0]+"""','')"""
                cursor.execute(sql)
                db.commit()
                db.close()
                d.update({dat : 1})
                if(division!='' and zone!= ''):
                    url='https://login.bulksmsgateway.in/sendmessage.php?user=username&password=password&mobile=number&message='+mobile+'&message='+repr(id)+" "+" Your Complaint is been forwarded to "+dept[0]+" and to the corresponding division "+division+'&sender=JANMTR&type=3'
                    webbrowser.open(url)
            else:
                url='https://login.bulksmsgateway.in/sendmessage.php?user=username&password=password&mobile=number&message='+mobile+'&message="Kindly Enter your PNR to register complaint"&sender=JANMTR&type=3'
                d.update({dat : 1})
                webbrowser.open(url)
        else:
            text = s[1][0:]
            pnr = data_helper.extract_pnr(text)
            tn = data_helper.extract_tn(text)
            var = ''
            if(s[0]=='I-complaint'):
                var = 'Visual'
            else:
                var = 'Audio'
            if(pnr!=None ):
                flag, division, zone = divZone.division_zone_classifier(pnr)
                if(flag==1):
                    continue
                dept = clf.predict({text})
                sql = """INSERT INTO comp(compid,
                   source,user,complaint,zone,division,department,status)
                   VALUES ('"""+repr(id)+"""', '"""+var+"""', '"""+''+"""', '"""+text+"""','"""+zone+"""','"""+division+"""','"""+dept[0]+"""','')"""
                cursor.execute(sql)
                db.commit()
                db.close()
            elif(tn!=None):
                division, zone = statictrain.stat(tn)
                dept = clf.predict({text})
                if(division ==''):
                    print("Invalid train number")
                sql = """INSERT INTO comp(compid,
                   source,user,complaint,zone,division,department,status)
                   VALUES ('"""+repr(id)+"""', '"""+var+"""', '"""+''+"""', '"""+text+"""','"""+zone+"""','"""+division+"""','"""+dept[0]+"""','')"""
                cursor.execute(sql)
                db.commit()
                db.close()
                d.update({dat : 1})
            else:
                d.update({dat : 1})
    time.sleep(10)
    

