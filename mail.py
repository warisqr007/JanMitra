import imaplib,time,string
import pymysql
db = pymysql.connect(host,user,password,database)
cursor = db.cursor()

T=time.time()
M = imaplib.IMAP4_SSL('imap.outlook.com',993)
user = your_mail_id
password = mail_password
M.login(user, password)
M.list()
d = {}
while(1):
    M.select("inbox")
    result, data = M.uid('search', None, "ALL") 
    latest_email_uid = data[0].split()[-1]
    result, data = M.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = data[0][1] 
    M.close()

    import email
    email_message = email.message_from_string(raw_email.decode('utf-8'))
    date = email_message['Date']
    s=email_message['Subject']
    s=s.split("/")
    if(date not in d.keys()):
        s=email_message['Subject']
        s=s.split("/")
        if(s[0]=='0'):
            sql = """UPDATE comp
                     SET status = 'Solved'
                     WHERE compid = '"""+s[1]+"""' """
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
        elif(s[0]=='1'):
            sql = """UPDATE comp
                     SET status = 'Unsolved'
                     WHERE compid = '"""+s[1]+"""' """
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
        else:
            sql = """UPDATE comp
                     SET status = '"""+s[0]+"""'
                     WHERE compid = '"""+(s[1])+"""' """
            print(sql)
            try:
               cursor.execute(sql)
               db.commit()
            except:
               db.rollback()
        d.update({date : 1})
        time.sleep(4)
        db.close()

