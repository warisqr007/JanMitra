import urllib.request, json,time,datetime
import pandas as pd
p = ''
q = ''
def stat(trn):	
	train = (trn)
	code = None
	
	df=pd.read_csv('classify.csv')

	with urllib.request.urlopen("https://api.railwayapi.com/v2/route/train/"+train+"/apikey/yourkey/") as url:
	    data = json.loads(url.read().decode())
	    if(len(data['route'])==0):
	    	return ('','')
	    r= []
	    r.append(data["route"])
	    code = r[0][0]['station']['code']
	if(code == None ):
	    print("Invalid Train Number")

	p=df[df['Station Code']==code]['Division']
	q=df[df['Station Code']==code]['Zone']
	p=p.to_string()
	p=''.join([i for i in p if not i.isdigit()])
	p=p.strip()
	q=q.to_string()
	q=''.join([i for i in q if not i.isdigit()])
	q=q.strip()
	return (p,q)