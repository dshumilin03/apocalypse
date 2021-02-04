import mysql.connector

cnx = mysql.connector.connect(user='f0509238_apocalypse_admin', password='QD3WVGmjUTugXzZ',
                              host='141.8.193.236',
                              database='f0509238_apocalypse')
cursor = cnx.cursor()

cursor.execute('update version set current_version = "1.0"')
cnx.commit()