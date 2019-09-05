import mysql.connector
myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
cur = myconn.cursor()
try:
    cur.execute("select * from fingerprints")
    result = cur.fetchall()
    for x in result:
        data=x[1];
except:
    myconn.rollback()
myconn.close()
text = open("dbtemp.txt","wb") 
text.write(str(data)) 
text.close()
print 'data has been written to text file'
