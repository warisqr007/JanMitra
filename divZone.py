import urllib.request, json,time,datetime
from datetime import datetime, timedelta
import pandas as pd

def division_zone_classifier(pnr):
    #pnr = (pn)
    DATE = None
    train = None
    station = None

    with urllib.request.urlopen("https://api.railwayapi.com/v2/pnr-status/pnr/"+pnr+"/apikey/yourkey/") as url:
        data = json.loads(url.read().decode())


        station = repr(data['boarding_point']['code'])
        train = (data['train']['number'])
    
        flag = 0
        p = ''
        q = ''
        if(train==None):
            flag = 1
            return (2,None,"Hello")
        else:
            count = 0
            with urllib.request.urlopen("https://api.railwayapi.com/v2/route/train/"+train+"/apikey/yourkey/") as url:
                dataa= json.loads(url.read().decode())
                r= []
                r.append(dataa["route"])
                l=len(r[0])

                for i in range(0,l):
                    if(r[0][i]['station']['code']== station):
                        count = int(r[0][i]['day'])
                        break;

            str = data['doj']
            p=str.split("-")
            t = datetime(int(p[2]),int(p[1]),int(p[0]), 0, 0)
            t=t-timedelta(days=count-1)
            d=t.strftime('%d-%m-%Y')
            DATE = d

            code = None
            with urllib.request.urlopen("https://api.railwayapi.com/v2/live/train/"+train+"/date/"+DATE+"/apikey/yourkey/") as url:
                    dataaa= json.loads(url.read().decode())
                    temp= dataaa['route']
                    l= len(temp)
                    for i in range(0,l):
                        if(temp[i]['has_departed']== False or temp[i]['has_arrived']== False):
                            code = temp[i]['station']['code']
                            break;


            df=pd.read_csv('classify.csv')
            p=df[df['Station Code']==code]['Division']
            q=df[df['Station Code']==code]['Zone']
            p=p.to_string()
            p=''.join([i for i in p if not i.isdigit()])
            p=p.strip()
            q=q.to_string()
            q=''.join([i for i in q if not i.isdigit()])
            q=q.strip()
       
        return (flag,p,q)