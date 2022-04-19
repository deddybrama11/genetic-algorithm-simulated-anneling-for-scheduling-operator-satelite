import random
import copy
import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
import math
import random
import copy
import matplotlib.pyplot as plt


jml  = [0.1,0.15,0.2,0.25,0.3,0.35,0.4]
y = [98.7,97,98.7,97.2,97.2,97.5,97.2]
print(jml)

# for ds in jml:
#
#     tmp = 0
#     conn = mysql.connect()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     qy = "SELECT * FROM `log_ga` WHERE suhu ="+str(ds)+" LIMIT 7"
#     cursor.execute(qy)
#     hari = cursor.fetchall()
#     cursor.close()
#     conn.close()
#
#     for s in hari:
#         tmp += s['time']
#         print(s['time'])
#     tmp = tmp/len(hari)
#     y.append(int(tmp))

print(y)
plt.title('Grafik pengujian learning rate terhadap Akurasi')
plt.xlabel('Learning Rate')
plt.ylabel('akurasi(%)')
plt.plot(jml,y,'g--d')

plt.show()



# jml  = [0.004,0.006,0.008,0.01,0.02]
# y = []
# print(jml)

# for ds in jml:
#
#     tmp = 0
#     conn = mysql.connect()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     qy = "SELECT * FROM `log_ga` WHERE individu ="+str(ds)+" LIMIT 6"
#     cursor.execute(qy)
#     hari = cursor.fetchall()
#     cursor.close()
#     conn.close()
#
#     for s in hari:
#         tmp += s['time']
#         print(s['time'])
#     tmp = tmp/len(hari)
#     y.append(int(tmp))
#
# print(y)
# plt.title('Grafik Pengaruh Individu terhadap Waktu')
# plt.xlabel('Individu')
# plt.ylabel('Execution Time')
# plt.plot(jml,y,'g--d')
#
# plt.show()


# yx = []
# tmp = 0
# conn = mysql.connect()
# cursor = conn.cursor(pymysql.cursors.DictCursor)
# qy = "SELECT * FROM `log_ga` WHERE mutation_rate BETWEEN 0.0039 AND 0.0041 AND individu =6 LIMIT 7"
# cursor.execute(qy)
# ha = cursor.fetchall()
# cursor.close()
# conn.close()
#
# for sd in ha:
#     tmp += sd['time']
#     print(sd['time'])
# tmp = tmp / len(ha)
# yx.append(int(tmp))
#
#
# tmp = 0
# conn = mysql.connect()
# cursor = conn.cursor(pymysql.cursors.DictCursor)
# qy = "SELECT * FROM `log_ga` WHERE mutation_rate BETWEEN 0.0059 AND 0.0061 AND individu =6 LIMIT 7"
# cursor.execute(qy)
# ha = cursor.fetchall()
# cursor.close()
# conn.close()
#
# for sd in ha:
#     tmp += sd['time']
#     print(sd['time'])
# tmp = tmp / len(ha)
# yx.append(int(tmp))
#
# tmp = 0
# conn = mysql.connect()
# cursor = conn.cursor(pymysql.cursors.DictCursor)
# qy = "SELECT * FROM `log_ga` WHERE mutation_rate BETWEEN 0.0079 AND 0.0081 AND individu =6 LIMIT 7"
# cursor.execute(qy)
# ha = cursor.fetchall()
# cursor.close()
# conn.close()
#
# for sd in ha:
#     tmp += sd['time']
#     print(sd['time'])
# tmp = tmp / len(ha)
# yx.append(int(tmp))
#
# tmp = 0
# conn = mysql.connect()
# cursor = conn.cursor(pymysql.cursors.DictCursor)
# qy = "SELECT * FROM `log_ga` WHERE mutation_rate BETWEEN 0.0099 AND 0.011 AND individu =6 LIMIT 7"
# cursor.execute(qy)
# ha = cursor.fetchall()
# cursor.close()
# conn.close()
#
# for sd in ha:
#     tmp += sd['time']
#     print(sd['time'])
# tmp = tmp / len(ha)
# yx.append(int(tmp))
#
#
# tmp = 0
# conn = mysql.connect()
# cursor = conn.cursor(pymysql.cursors.DictCursor)
# qy = "SELECT * FROM `log_ga` WHERE mutation_rate BETWEEN 0.019 AND 0.021 AND individu =6 LIMIT 7"
# cursor.execute(qy)
# ha = cursor.fetchall()
# cursor.close()
# conn.close()
#
# for sd in ha:
#     tmp += sd['time']
#     print(sd['time'])
# tmp = tmp / len(ha)
# yx.append(int(tmp))
#
# plt.title('Grafik Pengaruh mutation rate terhadap Waktu')
# plt.xlabel('Mutation Rate')
# plt.ylabel('Execution Time ( per-detik )')
# plt.plot(jml,yx,'g--d')
#
# plt.show()