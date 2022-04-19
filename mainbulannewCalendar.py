import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
import math
import random
import copy
import time
import datetime, calendar
from datetime import  datetime as dd

try:
    conn = mysql.connect()
    # Ambil satelit
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM satelit")
    satelit = cursor.fetchall()
    # Ambil hari
    cursor.execute("SELECT * FROM hari")
    hari1 = cursor.fetchall()
    # Ambil karyawan
    cursor.execute("SELECT * FROM karyawan")
    nip = cursor.fetchall()
    sf = "SELECT * FROM shift"
    cursor.execute(sf)
    shft = cursor.fetchall()
    shift = []
    for ia in (shft):
        shift.append(ia['shift'])

    job_krywn = {}
    for i in nip:
        tmp_2 = []
        tmp_nip = i['nip']
        for a in range(len(shift)):
            a = a + 1
            taa = "SELECT job from status_karyawan WHERE nip =" + i['nip'] + " AND shift = " + str(a)
            cursor.execute(taa)
            job = cursor.fetchall()
            tmp = []
            for adee in job:
                tmp.append(adee['job'])
            tmp_2.append(tmp)
        tm = {tmp_nip: tmp_2, }
        job_krywn.update(tm)
    print("job_karyawan : ", job_krywn)

    jb = {}
    for hr in hari1:
        h = hr['nama_hari']
        tmp = []
        for ia in range(len(shift)):
            tm = []
            ia += 1
            dws = "SELECT * FROM jadwal WHERE hari='" + h + "' AND shift =" + str(ia)
            cursor.execute(dws)
            d = cursor.fetchall()
            for i in d:
                ad = i['id_job']
                for b in range(i['jml']):
                    tm.append(ad)
            tmp.append(tm.copy())
        jb.update({h: tmp})

    for aw in jb:
        print(jb[aw])


except Exception as e:
    print(e)
finally:
    cursor.close()
    conn.close()

krywn = []
for aswa in nip:
    krywn.append(aswa['nip'])

@app.route('/add', methods=['POST'])
def add_user():
    try:
        _json = request.json
        _nip = _json['nip']
        _name = _json['nama']
        _jenis = _json['jenis']

        #save
        sql = "INSERT INTO karyawan(nip,nama,jenis_kelamin) VALUES(%s,%s,%s)"
        data =(_nip,_name,_jenis,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute()
        conn.commit()
        resp = jsonify('User added successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/user/<int:id>')
def user(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM karyawan WHERE nip=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/user')
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM karyawan")
        row = cursor.fetchall()
        print(row)
        for r in row:
            print("id : ", r['nip'])

        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def getHariBulanIni():
    currentYear = dd.now().year
    currentMonth = dd.now().month

    num_days = calendar.monthrange(currentYear, currentMonth)[1]
    days = [day for day in range(1, num_days + 1)]

    day_name = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

    hari_bulan_ini = []
    tmp_ar = []

    for i in range(len(days)):
        date = str(str(days[i]) + ' ' + str(currentMonth) + ' ' + str(currentYear))
        day = datetime.datetime.strptime(date, '%d %m %Y').weekday()

        if (i == 0 & day == 0):
            tmp_ar.append(day_name[day])
        elif (day == 0):
            hari_bulan_ini.append(tmp_ar.copy())
            tmp_ar.clear()
            tmp_ar.append(day_name[day])
        else:
            tmp_ar.append(day_name[day])

        if (i == (len(days) - 1)):
            if (len(tmp_ar) != 0):
                print("masuk")
                hari_bulan_ini.append(tmp_ar.copy())
                tmp_ar.clear()
    return hari_bulan_ini

def gen():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print(nip)

        #------------------------------ ambil karyawan ------------------- #



        #------------------------------ ambil shift --------------------------#

        shift = []
        for ia in (shft):
            shift.append(ia['shift'])


        #--------------- ambil job per karyawan ------------------#

        #variabel final


        # print(satelit)
        #--------------------------- ambil Tanggal Hari ini --------------------#

        currentYear = dd.now().year
        currentMonth = dd.now().month

        num_days = calendar.monthrange(currentYear, currentMonth)[1]
        days = [day for day in range(1, num_days + 1)]

        day_name = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

        hari_bulan_ini = []
        tmp_ar = []

        for i in range(len(days)):
            date = str(str(days[i]) + ' ' + str(currentMonth) + ' ' + str(currentYear))
            day = datetime.datetime.strptime(date, '%d %m %Y').weekday()

            if (i == 0 & day == 0):
                tmp_ar.append(day_name[day])
            elif (day == 0):
                hari_bulan_ini.append(tmp_ar.copy())
                tmp_ar.clear()
                tmp_ar.append(day_name[day])
            else:
                tmp_ar.append(day_name[day])

            if (i == (len(days) - 1)):
                if (len(tmp_ar) != 0):
                    print("masuk")
                    hari_bulan_ini.append(tmp_ar.copy())
                    tmp_ar.clear()

        # ---------------------------- generate random JADWAL ------------------ #
        indv2 = []
        for i in range(1, 7):
            for sat in satelit:
                s = sat['nama_satelit']
                #disini
                minggu = []
                for mg in hari_bulan_ini:
                    bbb = {}
                    for hr in mg:
                        h = hr
                        indx = next(item for item in hari1 if item["nama_hari"] == hr)
                        jml = indx['jumlah']
                        jml2 = indx['jumlah2']
                        check = checkKey(bbb, s)
                        if (bool(bbb) == False):
                            tmp = []
                            tmp2 = []
                            for i in range(jml):
                                tmp.append(random.choice(krywn.copy()))
                            for i in range(jml2):
                                tmp2.append(random.choice(krywn.copy()))
                            bbb = {s: {h: [tmp.copy(), tmp2.copy()], }, }.copy()
                        elif (check == False):
                            tmp = []
                            tmp2 = []
                            for i in range(jml):
                                tmp.append(random.choice(krywn.copy()))
                            for i in range(jml2):
                                tmp2.append(random.choice(krywn.copy()))
                            asd = {s: {h: [tmp.copy(), tmp2.copy()], }}.copy()
                            bbb.update(asd.copy())
                        else:
                            tmp = []
                            tmp2 = []
                            for i in range(jml):
                                tmp.append(random.choice(krywn.copy()))
                            for i in range(jml2):
                                tmp2.append(random.choice(krywn.copy()))
                            asd = {h: [tmp.copy(), tmp2.copy()]}.copy()
                            bbb[s].update(asd.copy())
                    minggu.append(bbb.copy())
            indv2.append(minggu.copy())

        # ------------------------ for DEBUGING ---------------------- #
        print("ini")
        for i in range(len(indv2)):
            for isd in indv2[i]:
                print(isd)
            print("")


        # print(indv['LAPAN-A2'])
        # print(indv['LAPAN-A3'])

        # evaluasi(indv2)
        # resp = jsonify(indv2)
        # resp.status_code = 200
        # return resp
        return indv2
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def checkKey(dict, key):
    if key in dict:
        return True
    else:
        return False
def evaluasi(indv2):
    count = []
    for indva in range(len(indv2)):
        ind = 0
        # print("======================== jarak per individu =====================")
        amrullah = '11'
        tempat_amrullah = 0
        for indv in indv2[indva]:
            for s,dict in indv.items():
                # print(s)
                for h,dict in indv[s].items():
                    bb = jb[h]
                    for i in range(len(indv[s][h])):
                        if amrullah in indv[s][h][i]:
                            tempat_amrullah += 1
                        if len(indv[s][h][i]) != len(set(indv[s][h][i])):
                            ind += 2
                        if i == 0:
                            check = [i for i in indv[s][h][i] if i in indv[s][h][1]]
                            ind += len(check)
                        for ads in range(len(indv[s][h][i])):
                            if bb[i][ads] in job_krywn[indv[s][h][i][ads]][i]:
                                pass
                            else:
                                ind += 3
        if tempat_amrullah != 2:
            tempat_amrullah-=2
            if tempat_amrullah<0:
                tempat_amrullah*=-1
                print(tempat_amrullah)
                ind+=tempat_amrullah
            else:
                ind+=tempat_amrullah
        count.append(ind)
    # print("Fitness : ",count)
    # print(min(count))
    # print("Elitisme index : ",count.index(min(count)))
    #============================= FITNES ========================#
    # fungsi fitness = (1/(1+fungsi_objektif))

    # print("Fungsi objective ( total fitness ) :",sum(count))

    fitness = []
    for i in count:
        fit = 1/(1+i)
        fitness.append(fit)
    # print("Sum fitnes :",sum(fitness))

    #========================= PROBABILITAS ====================#
    probabilitas = []
    for i in fitness:
        prob = i/sum(fitness)
        probabilitas.append(prob)
    #========================== CUMULATIVE PROBABILITAS ============#
    tm = 0
    cprobabilitas = []
    for i in probabilitas:
        tm += i
        cprobabilitas.append(tm)
    rw = []
    for i in range(len(fitness)-1):
        rw.append(random.uniform(0,1))
    #========================= ROULETE WHEEL =================#
    tempat = []
    tmmm = []
    for r in range(len(rw)):
        b = 0.0
        for i in range(len(cprobabilitas)):
            if ((i == 0) & (rw[r]< cprobabilitas[i])):
                if (b>cprobabilitas[i])|(b==0.0):
                    b=cprobabilitas[i]
            elif cprobabilitas[i-1]<rw[r]<cprobabilitas[i]:
                if ((b>cprobabilitas[i])|(b==0.0)):
                    b=cprobabilitas[i]
        tempat.append(b)
        a = cprobabilitas.index(b)
        tmmm.append(a)
    tmmm.insert(0,count.index(min(count)))
    # print("After Roulete Wheel :",tempat)
    print("Urutan : ",tmmm)

    indv3 = copy.deepcopy(indv2)

    for i in range(len(tmmm)):
        indv2[i] = copy.deepcopy(indv3[tmmm[i]])
    # print(indv3)
    # print(indv2)

    # print("Setelah Seleksi:")
    # for jkl in indv2:
    #      print(jkl)

    return indv2
    # crossover(indv2)

def crossover(indv2):
    # print("============================= BAGIAN CROSSOVER ===============================")
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT nama_hari FROM `hari` ORDER BY id_hari ASC")
    hari = cursor.fetchall()
    cursor.close()
    conn.close()

    pc = round(len(indv2)/2)
    t = []
    for i in range(len(indv2)):
        t.append(random.uniform(0,1))

    # print(t)
    tmept = []
    for jj in range(pc):
        jl = min(t)
        if t.index(jl) == 0:
            t[t.index(jl)] = 1
            jl = min(t)
            tmept.append(t.index(jl))
        else:
            tmept.append(t.index(jl))
            t[t.index(jl)] = 1
    print("tmpet = "+str(tmept))

    ackw = 0
    acka = 0
    prmg = 0
    for indva in range(len(indv2)):
        for indv in indv2[indva]:
            for s,dict in indv.items():
                # print('acka')
                # print(len(indv[s]))
                acka += int (len(indv[s]))
                # ackw = int (len(indv[s])*2)
                prmg = int (len(indv[s]))
                ackw += int(len(indv[s]))
                break
        break
    print("ackw = "+str(ackw))

    tm2 = []

    for v in tmept:
        ajks = copy.deepcopy(indv2[v])
        tm2.append(copy.deepcopy(ajks))

    acakArr = []
    for acak in range(len(tmept)):
        acakArr.append(random.randint(1,ackw-1))
    dd = tm2.copy()
    print("acakArr = "+str(acakArr))

    #======================================== MAIN CROSSOVER =========================#
    # Masih terdapat beberapa kesalahan seperti jika 1 ambil 2 , 2 ambil 3 maka 1 = 3
    #  jika random number (mmbc) < 7 maka hanya LAPAN-A2 yang akan di eksekusi, harusnya LAPAN-A3 juga
    #  khusus untuk random number nomor 7 ditempatkan pada hari minggu di LAPAN-A2
    # CROSSOVER ini MANUAL dengan menuliskan nama satelit
    # CROSSOVER DONE

    o = 0
    jrk_hari = []
    for indva in range(len(indv2)):
        for indv in indv2[indva]:
            for s,dict in indv.items():
                o += int (len(indv[s]))
                jrk_hari.append(o - 1)
                break
        break
    print("jrk_hari = "+str(jrk_hari))

    # o = 0
    # jrk_hari = []
    # while o < acka:
    #     o += 7
    #     jrk_hari.append(o-1)

    hari_bulan_ini = getHariBulanIni()

    indx = []
    for mg in hari_bulan_ini:
        bbb = []
        for hr in mg:
            h = hr
            bbb.append(hr)
        indx.append(bbb.copy())
        bbb.clear()
    print("indx = "+str(indx))

    for bv in range(len(tm2)):
        posisi = 0
        indx_jrk_hari = 0
        for i in jrk_hari:
            if i >= acakArr[bv]:
                posisi=jrk_hari.index(i)
                indx_jrk_hari = i
                break
        pj = int(len(tm2))
        print("pj = "+str(pj))
        if ((bv+1)<pj):
            tmpp = 0
            if posisi != 0:
                tmpp = acakArr[bv]-jrk_hari[posisi-1]
                print(tmpp)
            else:
                tmpp =acakArr[bv]
            for i in range(posisi,len(tm2[0])):
            # for i in range(posisi, 4):
                while tmpp<=len(tm2[0][i])-1:
                # while tmpp <= 7:
                    h = indx[posisi][tmpp]
                    tempat = (tm2[bv +1][i]['LAPAN-A2'][h]).copy()
                    dd[bv][i]['LAPAN-A2'][h] = tempat.copy()
                    tmpp+=1
                tmpp=1
        else:
            tmpp = 0
            if posisi != 0:
                tmpp = acakArr[bv] - jrk_hari[posisi - 1]
            else:
                tmpp = acakArr[bv]
            for i in range(posisi, 4):
                while tmpp <= 7:
                    h = hari[tmpp - 1]
                    hri = (h['nama_hari'])
                    tempat = (tm2[0][i]['LAPAN-A2'][hri]).copy()
                    dd[bv][i]['LAPAN-A2'][hri] = tempat.copy()
                    tmpp += 1
                tmpp = 1

    dx = 0
    for x in tmept:
        indv2[x] = (dd[dx]).copy()
        # print(indv2[x])
        dx +=1

    for i in indv2:
        print(i)
    return indv2


def mutasi(indv2):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT nama_hari FROM `hari` ORDER BY id_hari ASC")
    hari = cursor.fetchall()
    cursor.close()
    conn.close()
    # print("============================ BAGIAN MUTASI =============================")

    juml = 0
    #Menghitung total gen x populasi
    for saw in range(len(indv2[0])):
        for jd in indv2[0][saw]:
            for nn in indv2[0][saw][jd]:
                for ias in indv2[0][saw][jd][nn]:
                    juml += len(ias)
    jum = juml*len(indv2)
    print(juml)
    print("Jumlah gen : ",jum);


    # juml = 0
    # for kk in indv2[0]:
    #     for kll in indv2[0][kk]:
    #         for ks in indv2[0][kk][kll]:
    #             # print(ks)
    #             # print(len(ks))
    #             juml += len(ks)
    # jum = juml*len(indv2)
    # print(juml)
    # print("Jumlah gen pada populasi : ",jum)
    #
    # print(math.floor(jum*0.08))

    #================Generate random posisi===============
    acakMut = []
    for acak in range(math.floor(jum*0.004)):
        ct = random.randint((juml+1), jum)
        while ct in acakMut:
            ct = random.randint((juml+1), jum)
        acakMut.append(ct)

    # print(acakMut)

    #====== ambil berapa jumlah per hari lalu dimasukkan ke ARRAY ====#
    # konsepnya adalah agar bisa menentukan posisi dari random posisi #

    hari_k = []
    totalGen = 0
    for asdw in indv2[0][0]:
        tm = 0
        for dino in indv2[0][0][asdw]:
            for weje in indv2[0][0][asdw][dino]:
                # print(len(weje))
                tm += len(weje)
                totalGen += len(weje)
            hari_k.append(tm)
    # print(totalGen)
    print("Hari_k : ",hari_k)
    print("Total gen : ",totalGen)

    indv_indx = []

    for iz in range(math.floor(jum*0.004)):
        indv_indx.append(random.randint(1, len(indv2)-1))
    # print(("indv index : ",indv_indx))

    indv_minggu = []
    for im in range(math.floor(jum*0.004)):
        indv_minggu.append(random.randint(0,len(indv2[0])-1))
    # print(("indv minggu : ",indv_minggu))

    indv_gen = []
    for ida in range(math.floor(jum*0.004)):
        indv_gen.append(random.randint(1,totalGen))
    # print(("indv gen : ",indv_gen))


    #==================== MAIN MUTASI ==============#

    for i in range(len(indv_gen)):
        for batas in range(len(hari_k)):
            # print(batas)
            if hari_k[batas]>=indv_gen[i]:
                if(batas==0):
                    selisih = indv_gen[i]
                else:
                    selisih = (indv_gen[i] - hari_k[batas-1])

                pdhari = hari[batas]['nama_hari']

                if len(indv2[indv_indx[indv_indx[i]]][indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0])>= selisih:
                    sdw = indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0]
                    sdw2 = indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][1]
                    sdw[selisih-1] = random.choice(krywn)
                    tmpt = {pdhari:[sdw,sdw2]}
                    indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'].update(tmpt)
                else:
                    sdw = indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][1]
                    selisih = (selisih - len(indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0]))
                    sdw[selisih-1] = random.choice(krywn)
                    sdw2 = indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0]
                    tmpt = {pdhari:[sdw2,sdw]}
                    indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'].update(tmpt)
                break

    return indv2
def prob_gen(indv2):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT nama_hari FROM `hari` ORDER BY id_hari ASC")
    hari = cursor.fetchall()
    cursor.close()
    conn.close()
    juml = 0
    for kk in indv2[0]:
        for kll in indv2[0][kk]:
            for ks in indv2[0][kk][kll]:
                # print(ks)
                # print(len(ks))
                juml += len(ks)
    jum = juml*len(indv2)
    # print(juml)
    # print("Jumlah gen pada populasi : ",jum)
    #
    # print(math.floor(jum*0.08))

    # ================Generate random posisi===============

    acakMut = []
    for acak in range(math.floor(jum * 0.008)):
        ct = random.randint((juml + 1), jum)
        while ct in acakMut:
            ct = random.randint((juml + 1), jum)
        acakMut.append(ct)

    # print(acakMut)

    # ====== ambil berapa jumlah per hari lalu dimasukkan ke ARRAY ====#
    # konsepnya adalah agar bisa menentukan posisi dari random posisi #

    hari_k = []
    totalGen = 0
    for asdw in indv2[0]:
        tm = 0
        for dino in indv2[0][asdw]:
            for weje in indv2[0][asdw][dino]:
                # print(len(weje))
                tm += len(weje)
                totalGen += len(weje)
            hari_k.append(tm)


    indv_minggu = []
    for im in range(math.floor(jum * 0.008)):
        indv_minggu.append(random.randint(0, len(indv2) - 1))
    # print(("indv minggu : ",indv_minggu))

    indv_gen = []
    for ida in range(math.floor(jum * 0.008)):
        indv_gen.append(random.randint(1, juml))
    # print(("indv gen : ",indv_gen))

    # ==================== MAIN MUTASI ==============#

    for i in range(len(indv_gen)):
        for batas in range(len(hari_k)):
            # print(batas)
            if hari_k[batas] >= indv_gen[i]:
                if (batas == 0):
                    selisih = indv_gen[i]
                else:
                    selisih = (indv_gen[i] - hari_k[batas - 1])

                pdhari = hari[batas]['nama_hari']

                if len(indv2[indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0]) >= selisih:
                    sdw = indv2[indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0]
                    sdw2 = indv2[indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][1]
                    sdw[selisih - 1] = random.choice(krywn)
                    tmpt = {pdhari: [sdw, sdw2]}
                    indv2[indv_minggu[i]]['LAPAN-A2'].update(tmpt)
                else:
                    sdw = indv2[indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][1]
                    selisih = (selisih - len(indv2[indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0]))
                    sdw[selisih - 1] = random.choice(krywn)
                    sdw2 = indv2[indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0]
                    tmpt = {pdhari: [sdw2, sdw]}
                    indv2[indv_minggu[i]]['LAPAN-A2'].update(tmpt)
                break

    return indv2

def energi_hitung(indv2):
    count = 0
    ind = 0
    amrullah = '11'
    tempat_amrullah = 0
    for indv in indv2:
        for s, dict in indv.items():
            for h, dict in indv[s].items():
                bb = jb[h]
                for i in range(len(indv[s][h])):
                    if amrullah in indv[s][h][i]:
                        tempat_amrullah += 1
                    if len(indv[s][h][i]) != len(set(indv[s][h][i])):
                        ind += 2
                    if i == 0:
                        check = [i for i in indv[s][h][i] if i in indv[s][h][1]]
                        ind += len(check)
                    for ads in range(len(indv[s][h][i])):
                        if bb[i][ads] in job_krywn[indv[s][h][i][ads]][i]:
                            pass
                        else:
                            ind += 3
        if tempat_amrullah != 2:
            tempat_amrullah -= 2
            if tempat_amrullah < 0:
                tempat_amrullah *= -1
                print(tempat_amrullah)
                ind += tempat_amrullah
            else:
                ind += tempat_amrullah
    count += ind
    return count
def sa(indv):
    iterasi = 1000000
    suhu_new = 3
    suhu = 3
    alpha = 0.980
    energi_tmp = 1
    while(energi_tmp == 1):
        energi = energi_hitung(indv)
        prob_indv = prob_gen(copy.deepcopy(indv))
        energi2 = energi_hitung(prob_indv)
        if(energi>energi2):
            indv = copy.deepcopy(prob_indv)
            suhu = suhu * alpha
            if((energi==0) | (iterasi<0)):
                energi_tmp = 0
            iterasi -= 1
        else:
            kemungkinanSolusi = math.exp((energi-energi2)/suhu)
            p = random.uniform(0,1)
            if(kemungkinanSolusi>p):
                indv = copy.deepcopy(prob_indv)
            else:
                indv = indv
            suhu = suhu * alpha
            if ((energi == 0) | (iterasi<0)):
                energi_tmp = 0
            iterasi -= 1
        if(suhu == suhu_new):
            suhu = 3
        suhu_new = copy.deepcopy(suhu)
    return indv


@app.route('/ga')
def ga():
    start_time = time.time()
    dsjdsw = gen()


    mySql_insertLog_query = """DELETE FROM jadwal_karyawan"""
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(mySql_insertLog_query)
    conn.commit()

    print("print ga testtingg bismillah")
    print(dsjdsw)
    looping = 0
    eval = {}
    cross = {}
    ft = 1
    while(ft == 1):
        eval = evaluasi(dsjdsw)
        cross = crossover(eval)
        dsjdsw = mutasi(cross)
        count = []
        looping+=1
        for indva in range(len(dsjdsw)):
            ind = 0
            amrullah = '11'
            tempat_amrullah = 0
            for indv in dsjdsw[indva]:
                for s, dict in indv.items():
                    for h, dict in indv[s].items():
                        bb = jb[h]
                        for i in range(len(indv[s][h])):
                            if len(indv[s][h][i]) != len(set(indv[s][h][i])):
                                ind += 2
                                print(h," shift ke ",i," ada duplikat !")
                            if amrullah in indv[s][h][i]:
                                tempat_amrullah+=1
                            if i == 0:
                                check = [i for i in indv[s][h][i] if i in indv[s][h][1]]
                                ind += len(check)
                                if(len(check)>0):
                                    print("ada lebih di ",indv[s][h][i]," dan ",indv[s][h][1])
                            for ads in range(len(indv[s][h][i])):
                                if bb[i][ads] in job_krywn[indv[s][h][i][ads]][i]:
                                    pass
                                else:
                                    ind += 3
                                    print("job karyawan salah pada minggu ke ",indva,"shift ke ",i," index ke ",ads)

            if tempat_amrullah != 2:
                tempat_amrullah -= 2
                if tempat_amrullah < 0:
                    tempat_amrullah *= -1
                    print(tempat_amrullah)
                    ind += tempat_amrullah
                else:
                    ind += tempat_amrullah
            count.append(ind)
        print("Fitness : ", count)
        print(looping)
        print("Fitness 2 : ",count)
        if ((count[0] == 0) | (looping> 8000)):
            ft = 0
        else:
            pass


    print(looping)
    # print(dsjdsw)
    for wwa in dsjdsw:
        print(wwa)

    for indva in range(len(dsjdsw)):
        indvi = dsjdsw[indva]
        break

    indiv_real = sa(indvi)
    last_fitnes = energi_hitung(indiv_real)


    record_toinsert = []
    for indva in range(len(dsjdsw)):
        mingguke = 1
        print(indva)
        for indv in dsjdsw[indva]:
            print("===== Minggu ke : ", mingguke, "=========")
            for s, dict in indv.items():
                for h, dict in indv[s].items():
                    # bb = jb[h]
                    # print(bb)
                    print("hari : ", h)
                    for i in range(len(indv[s][h])):
                        print(indv[s][h][i])
                        for nip in indv[s][h][i]:
                            a = (mingguke, h, str((i + 1)), nip)
                            record_toinsert.append(a)
            mingguke += 1
        break
    print(record_toinsert)





    mySql_insert_query = """INSERT INTO jadwal_karyawan(minggu_ke, hari, shift, nip) 
                               VALUES (%s, %s, %s, %s) """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.executemany(mySql_insert_query, record_toinsert)
    conn.commit()

    print("--- %s seconds ---" % (time.time() - start_time))
    waktu = (time.time() - start_time)
    print("Waktu adalah : ", waktu)
    record_toinsertLog = []

    vlue = (0.004, 6, last_fitnes, waktu, 3, 0.980)
    record_toinsertLog.append(vlue)
    mySql_insertLog_query = """INSERT INTO log_ga(mutation_rate, individu, fitness, time, suhu, alpha) 
                                       VALUES (%s, %s, %s, %s, %s, %s) """
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.executemany(mySql_insertLog_query, record_toinsertLog)
    conn.commit()



    resp = jsonify(dsjdsw)
    resp.status_code = 200
    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status' : 404,
        'message' : 'Tidak ditemukan :' +request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
