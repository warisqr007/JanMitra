import re

def clean_text(text):
    text = re.sub(r"(?:\@|pic.twitter.com|https?\://)\S+", "", text)
    text = text.replace('\\n',' ')
    text = text.strip()
    text = text.lower()
    
    return text

def extract_pnr(text):
    tokens = re.split(r'\W+', text)
    
    pnr = [s for s in tokens if s.isdigit() and len(s)==10]
    flag = 0
    for i in range(len(tokens)):
        if (tokens[i].isdigit() and len(tokens[i])==10):
            if (i>=2 and (tokens[i-1] == 'pnr' or tokens[i-2] == 'pnr')):
                pnr = tokens[i]
                flag = 1
                break
    if(flag):
        return pnr
    else:
        if(pnr):
            return pnr[0]
    return None

def extract_tn(text):
    tokens = re.split(r'\W+', text)
    
    tn = [s for s in tokens if s.isdigit() and len(s)==5]
    if(tn):
        return tn[0]
    else:
    	return None
        
    