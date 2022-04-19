import datetime, calendar
from datetime import  datetime as dd
from db_config import mysql
import pymysql

conn = mysql.connect()
cursor = conn.cursor(pymysql.cursors.DictCursor)
cursor.execute("SELECT * FROM hari")
hari1 = cursor.fetchall()
# Ambil karyawan
print(hari1)
print(next(item for item in hari1 if item["nama_hari"] == "Senin"))


currentYear = dd.now().year
currentMonth = dd.now().month

num_days = calendar.monthrange(currentYear, currentMonth)[1]
days = [day for day in range(1, num_days+1)]

day_name= ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu','Minggu']

hari_bulan_ini = []
tmp_ar = []

for i in range(len(days)):
    date=str(str(days[i])+' '+str(currentMonth)+' '+str(currentYear))
    day = datetime.datetime.strptime(date, '%d %m %Y').weekday()

    if(i == 0 & day==0):
        tmp_ar.append(day_name[day])
    elif(day==0):
        tanda=0
        hari_bulan_ini.append(tmp_ar.copy())
        tmp_ar.clear()
        tmp_ar.append(day_name[day])
    else:
        tmp_ar.append(day_name[day])


    if(i==(len(days)-1)):
        if(len(tmp_ar)!=0):
            print("masuk")
            hari_bulan_ini.append(tmp_ar.copy())
            tmp_ar.clear()


print(hari_bulan_ini)