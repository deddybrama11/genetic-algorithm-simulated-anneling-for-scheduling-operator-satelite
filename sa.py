import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
import math
import random
import copy
import time

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
    krywn.append(aswa['nip'])\

def checkKey(dict, key):
    if key in dict:
        return True
    else:
        return False

def gen_sa():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        print(nip)

        shift = []
        for ia in (shft):
            shift.append(ia['shift'])

        indv2 = []
        for i in range(0, 1):

            for sat in satelit:
                s = sat['nama_satelit']
                for mg in range(0,4):
                    bbb = {}

                    for hr in hari1:
                        h = hr['nama_hari']
                        jml = hr['jumlah']
                        jml2 = hr['jumlah2']
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
                    indv2.append(bbb.copy())

        print("ini")
        # for i in range(len(indv2)):
        #
        # for isd in indv2:
        #     print(isd)

        return indv2
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def prob_gen(indv2):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT nama_hari FROM `hari` ORDER BY id_hari ASC")
    hari = cursor.fetchall()
    cursor.close()
    conn.close()
    # print("============================ BAGIAN MUTASI =============================")

    # for cx in indv2:
    #     print(cx)

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
    # print(totalGen)
    # print("Hari_k : ",hari_k)
    # print("Total gen : ", totalGen)


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
                    # print("")
                    # print("Index gen ke 0-",(selisih-1))
                    tmpt = {pdhari: [sdw, sdw2]}
                    indv2[indv_minggu[i]]['LAPAN-A2'].update(tmpt)
                else:
                    sdw = indv2[indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][1]
                    selisih = (selisih - len(indv2[indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0]))
                    sdw[selisih - 1] = random.choice(krywn)
                    # print("Index gen ke 1-", (selisih - 1))
                    sdw2 = indv2[indv_minggu[i]]['LAPAN-A2'][hari[batas]['nama_hari']][0]
                    tmpt = {pdhari: [sdw2, sdw]}
                    indv2[indv_minggu[i]]['LAPAN-A2'].update(tmpt)
                break

    # for fx in indv2:
    #     print(fx)

    return indv2

def eval(indv2):
    count = 0
    # print("================ BAGIAN EVALUASI ===============")
    # print(indv2)
    # for indva in range(len(indv2)):
    ind = 0

    amrullah = '11'
    tempat_amrullah = 0
    for indv in indv2:

        for s, dict in indv.items():
            # print(s)
            for h, dict in indv[s].items():
                bb = jb[h]
                for i in range(len(indv[s][h])):
                    # print(i)
                    # print(indv[s][h][i])
                    if amrullah in indv[s][h][i]:
                        tempat_amrullah += 1
                    if len(indv[s][h][i]) != len(set(indv[s][h][i])):
                        ind += 2
                        # print(h," shift ke ",i," ada duplikat !")
                    if i == 0:
                        check = [i for i in indv[s][h][i] if i in indv[s][h][1]]
                        ind += len(check)
                    for ads in range(len(indv[s][h][i])):
                        # print(indv[s][h][i][ads])
                        # print(job_krywn[indv[s][h][i][ads]][i])
                        # print("jadwal harian ",bb[i])
                        # print("ads : ",ads)
                        # print("butuh sekian : ",bb[i][ads])
                        if bb[i][ads] in job_krywn[indv[s][h][i][ads]][i]:
                            pass
                        else:
                            ind += 3
                        # for t in range(len(bb[i])):
                        #     print("butuh : ",bb[i][t])
        if tempat_amrullah != 2:
            tempat_amrullah -= 2
            if tempat_amrullah < 0:
                tempat_amrullah *= -1
                print(tempat_amrullah)
                ind += tempat_amrullah
            else:
                ind += tempat_amrullah
    count += ind
    # print(" count : ",ind)

    return count

# def nextGen(indv2, indv_prob):
#     if


def sa(indv):
    iterasi = 0
    suhu = 10000000
    indv = gen_sa()
    alpha = 0.995

    while(iterasi<10000000000000000):

        energi = eval(indv)
        prob_indv = prob_gen(copy.deepcopy(indv))
        energi2 = eval(prob_indv)
        print("suhu : ",suhu)

        if(energi>energi2):
            indv = copy.deepcopy(prob_indv)
            iterasi=+1
            print("energi 1 lebih")
        else:
            print("energi 2 lebih dari")
            kemungkinanSolusi = math.exp((energi-energi2)/suhu)
            print(kemungkinanSolusi)
            p = random.uniform(0,1)
            if(kemungkinanSolusi>p):
                indv = copy.deepcopy(prob_indv)
            else:
                indv = indv
            suhu = suhu * alpha
            iterasi =+ 1

        print(energi)
        print(energi2)
        print("")

sa()