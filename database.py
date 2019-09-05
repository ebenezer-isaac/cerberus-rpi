import mysql.connector    
myconn = mysql.connector.connect(host = "192.168.0.5", user = "root",passwd = "cerberus",database = "cerberus")  
cur = myconn.cursor()  
try:      
    cur.execute("select * from student")   
    result = cur.fetchall()  
    for x in result:  
        print(x);  
except:  
    myconn.rollback()  
myconn.close()