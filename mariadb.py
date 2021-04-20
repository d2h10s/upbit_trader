import pymysql

conn = None
cur = None

sql = ""

conn = pymysql.connect(host='127.0.0.1', user='root', password='hail', db='upbit', charset='utf8') # 접속정보

cur = conn.cursor()
'''
sql = "CREATE TABLE IF NOT EXISTS upbit_token (id char(20), access_key char(41), secret_key char(41))" 
cur.execute(sql) 
sql = "insert into upbit_token values('home', 'igVDxSWVHawc0NSeG4GlwByqIwMCeKgNl55xjxpN', 'z6aqN8xvht4xY99VNsuCsbcxqgI2z0JdHxGgnixx')"
cur.execute(sql) 
sql = "insert into upbit_token values('lab', 'uzm9Y88q9Giq9Pr3LAL4orkDEoLAuHjvUL2VuToo', 'xhxWXYL0qNU5JcwUIJFa1jyfpG7pSXWm8sLKaqe5')"
'''
#cur.execute("INSERT OR REPLACE stock VALUES ('EEP', NOW(), NOW()) ON DUPLICATE KEY UPDATE currency='EEP', datetime='2021-02-22 20:23:14', price='234'")
cur.execute("REPLACE into stock VALUES ('BAT',NOW(), '772')")
#cur.execute("INSERT INTO stock IF NOT EXISTS (SELECT * FROM stock WHERE currency='XRP') VALUES('BIT','2021-02-22 20:23:14', '234')")
row = cur.fetchone()
print(row)
conn.commit() # 저장
conn.close() # 종료
