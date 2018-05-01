import pandas as pd
import numpy as np
import data_helper
import divZone
from sklearn.externals import joblib
import tweepy
import time
import pymysql,sys
import statictrain
from googletrans import Translator
translator = Translator()

clf = joblib.load('svm_tweet.pkl') 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth)

db = pymysql.connect(host,user,password,database)
cursor = db.cursor()
d = {}
id = 1
while(1):
    mentions = api.mentions_timeline(count=1)
    i=1

    for mention in tweepy.Cursor(api.mentions_timeline).items():
        cursor = db.cursor()
        if(i==0):
            break;
        if((mention.id_str not in d.keys())):
            
            temp = data_helper.clean_text(mention.text)
            res=translator.translate(temp, dest='en')
            text = res.text
            pnr = data_helper.extract_pnr(text)
            tn = data_helper.extract_tn(text)
            if(pnr!=None ):
                flag, division, zone = divZone.division_zone_classifier(pnr)
                if(flag==1):
                    continue

                print(division)
                dept = clf.predict({text})
                sql = """INSERT INTO comp(compid,
                   source,user,complaint,zone,division,department,status)
                   VALUES ('"""+repr(id)+"""', 'Twitter', '"""+mention.user.screen_name+"""', '"""+(mention.text)+"""','"""+zone+"""','"""+division+"""','"""+dept[0]+"""','')"""
                print(sql)
                d.update({mention.id_str : 1})
                api.update_status("@" + mention.user.screen_name +" Your Complaint is been forwarded to "+dept[0]+" and to the corresponding division "+division , in_reply_to_status_id = mention.id_str)
                
                cursor.execute(sql)
                db.commit()
                url='https://login.bulksmsgateway.in/sendmessage.php?user=username&password=password&mobile=number&message='+repr(id)+" "+mention.text+'&sender=sender&type=3'
                id=id+1
                import webbrowser
                webbrowser.open(url)
            elif(tn!=None):
            
                division, zone = statictrain.stat(tn)
                dept = clf.predict({text})
                d.update({mention.id_str : 1})
                if(division!='' and zone!= ''):
                    api.update_status("@" + mention.user.screen_name +" Your Complaint is been forwarded to "+dept[0]+" and to the corresponding division "+division , in_reply_to_status_id = mention.id_str)
                    url='https://login.bulksmsgateway.in/sendmessage.php?user=username&password=password&mobile=number&message='+repr(id)+" "+mention.text+'&sender=sender&type=3'
                    import webbrowser
                    webbrowser.open(url)
            else:
                d.update({mention.id_str : 1})
                api.update_status("@" + mention.user.screen_name +" Please enter pnr number.", in_reply_to_status_id = mention.id_str)
        i=i-1;
        
    time.sleep(10)
    db.close()