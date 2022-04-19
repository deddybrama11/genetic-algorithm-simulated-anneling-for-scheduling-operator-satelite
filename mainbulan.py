import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request
import math
import random
import copy

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
        #--------------------------- ambil JOB jadwal --------------------#

        # ---------------------------- generate random JADWAL ------------------ #
        indv2 = []
        for i in range(1, 9):

            for sat in satelit:
                s = sat['nama_satelit']
                #disini
                minggu = []
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
    # print("================ BAGIAN EVALUASI ===============")
    # print(indv2)
    for indva in range(len(indv2)):
        ind = 0
        # print("======================== jarak per individu =====================")
        # print(indv)
        amrullah = '11'
        tempat_amrullah = 0
        for indv in indv2[indva]:

            for s,dict in indv.items():
                # print(s)
                for h,dict in indv[s].items():
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
        # if tempat_amrullah != 2:
        #     tempat_amrullah-=2
        #     if tempat_amrullah<0:
        #         tempat_amrullah*=-1
        #         print(tempat_amrullah)
        #         ind+=tempat_amrullah
        #     else:
        #         ind+=tempat_amrullah
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
    # P[i] = fitness[i] / total_fitness

    probabilitas = []
    for i in fitness:
        prob = i/sum(fitness)
        probabilitas.append(prob)
    # print("Probabilitas :",probabilitas)

    #========================== CUMULATIVE PROBABILITAS ============#
    tm = 0
    cprobabilitas = []
    for i in probabilitas:
        tm += i
        cprobabilitas.append(tm)
    # print("Cumulative Probabilitas(cprob): ",cprobabilitas)

    rw = []
    for i in range(len(fitness)-1):
        rw.append(random.uniform(0,1))
    # print("Random number(rw) :",rw)
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
    # Ambil hari

    # print("")
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

    # print("Individu yang akan di CROSSOVER ( tmept ) :")
    # print(tmept)

    ackw = 0
    acka = 0
    prmg = 0
    for indva in range(len(indv2)):
        for indv in indv2[indva]:
            for s,dict in indv.items():
                acka += int (len(indv[s]))
                # ackw = int (len(indv[s])*2)
                prmg = int (len(indv[s]))
                ackw += int(len(indv[s]))
                break
        break

    # print(ackw)
    # print(acka)

    tm2 = []
    # print("testing liat individu")

    # print("")

    for v in tmept:
        ajks = copy.deepcopy(indv2[v])
        tm2.append(copy.deepcopy(ajks))
    # print("Random yang akan di crossover indv : ", tmept)
    # print("Random yang akan di crossover : ")
    # for mmn in tm2:
    #     print(mmn)
    # print("")


    acakArr = []
    for acak in range(len(tmept)):
        acakArr.append(random.randint(1,ackw-1))


    # print("Posisi Gen CROSSOVER : ",acakArr)
    dd = tm2.copy()

    #======================================== MAIN CROSSOVER =========================#
    # Masih terdapat beberapa kesalahan seperti jika 1 ambil 2 , 2 ambil 3 maka 1 = 3
    #  jika random number (mmbc) < 7 maka hanya LAPAN-A2 yang akan di eksekusi, harusnya LAPAN-A3 juga
    #  khusus untuk random number nomor 7 ditempatkan pada hari minggu di LAPAN-A2
    # CROSSOVER ini MANUAL dengan menuliskan nama satelit
    # CROSSOVER DONE

    o = 0
    jrk_hari = []
    while o < acka:
        o += 7
        jrk_hari.append(o-1)

    # print("JARAK minggu : ",jrk_hari)

    for bv in range(len(tm2)):
        # print("==================indv ke ",bv,"===================")
        # print(bv)
        posisi = 0
        for i in jrk_hari:
            if i >= acakArr[bv]:
                posisi=jrk_hari.index(i)
                break
        # print(posisi)
        pj = int(len(tm2))

        # print("Jika ",(bv+1)," < ",pj)
        if ((bv+1)<pj):
            tmpp = 0
            if posisi != 0:
                tmpp = acakArr[bv]-jrk_hari[posisi-1]
            else:
                tmpp =acakArr[bv]

            for i in range(posisi,4):
                # print("Posisi = ",i)
                while tmpp<=7:
                    h = hari[tmpp-1]
                    hri = (h['nama_hari'])
                    # print(hri)
                    tempat = (tm2[bv +1][i]['LAPAN-A2'][hri]).copy()
                    dd[bv][i]['LAPAN-A2'][hri] = tempat.copy()
                    tmpp+=1
                tmpp=1

        else:
            tmpp = 0
            if posisi != 0:
                tmpp = acakArr[bv] - jrk_hari[posisi - 1]
            else:
                tmpp = acakArr[bv]

            for i in range(posisi, 4):
                # print("Posisi = ", i)
                while tmpp <= 7:
                    h = hari[tmpp - 1]
                    hri = (h['nama_hari'])
                    # print(hri)
                    tempat = (tm2[0][i]['LAPAN-A2'][hri]).copy()
                    dd[bv][i]['LAPAN-A2'][hri] = tempat.copy()
                    tmpp += 1
                tmpp = 1
                # print("")

    # print("Setelah di crossover : ")
    # for mmdsn in dd:
    #     print(mmdsn)
    # print("")

    dx = 0
    for x in tmept:
        # print(x)
        indv2[x] = (dd[dx]).copy()
        dx +=1

    # print("Total Setelah Crossover :")
    # for hh in indv2:
    #     print(hh)

    return indv2
    # mutasi(indv2)

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
    print(("indv index : ",indv_indx))

    indv_minggu = []
    for im in range(math.floor(jum*0.004)):
        indv_minggu.append(random.randint(0,len(indv2[0])-1))
    print(("indv minggu : ",indv_minggu))

    indv_gen = []
    for ida in range(math.floor(jum*0.004)):
        indv_gen.append(random.randint(1,totalGen))
    print(("indv gen : ",indv_gen))


    #==================== MAIN MUTASI ==============#

    for i in range(len(indv_gen)):
        for batas in hari_k:
            # print(batas)
            if batas>=indv_gen[i]:
                selisih = (batas - indv_gen[i])+1
                if selisih>batas:
                    print("kapan kesininya")
                    selisih-=1
                else:
                    pass

                pdhari = hari[hari_k.index(batas)]['nama_hari']
                # print(pdhari)
                if len(indv2[indv_indx[indv_indx[i]]][indv_minggu[i]]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1])>= selisih:
                    # print(i)
                    # print(batas)
                    # print("mutasi pada index ke - 1")
                    # selisih *= -1
                    sdw = indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1]
                    # print(sdw)
                    # print(sdw[selisih])
                    sdw2 = indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][0]
                    sdw[selisih] = random.choice(krywn)
                    tmpt = {pdhari:[sdw2,sdw]}
                    indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'].update(tmpt)
                    # print("berhasil <<")
                else:
                    # print(i)
                    # print(batas)
                    # print("mutasi pada index ke - 0")
                    sdw = indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][0]
                    selisih = (selisih - len(indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1]))*-1
                    # print(sdw)
                    # print(sdw[selisih])
                    sdw[selisih] = random.choice(krywn)
                    sdw2 = indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1]
                    tmpt = {pdhari:[sdw,sdw2]}
                    indv2[indv_indx[i]][indv_minggu[i]]['LAPAN-A2'].update(tmpt)
                    # print("berhasi;><><><><><>")

                # print("Selisih : ",batas-itm)
                # print('============================================')
                break
                #ambil index hari
                #taruh di hari['nama_hari']
        #Jika random number diatas 74
        else:
            # print(itm-math.floor(itm/totalGen)*totalGen)

            indx=math.floor(itm/totalGen)
            if indx == len(indv2):
                indx = indx-1
                # print("DHJSAHDJSADJSADJSAHD --- PANJANG index--- ", indx, "--", len(indv2))
            else:
                pass
            # print(indx)
            items = itm-indx*totalGen
            # ------------------------------------------------ ADA KESALAHAN DISINI ---- INDEX KE 6 444 JADI KE 5 DAN HARI SENIN, HARUSNYA HARI MINGGU --------


            for batas in hari_k:
                # print(batas)
                if batas>=items:
                    selisih = (batas - items)+1
                    if selisih>batas:
                        selisih-=1
                    else:
                        pass
                    # print(hari_k.index(batas))
                    pdhari = hari[hari_k.index(batas)]['nama_hari']
                    # print(pdhari)

                    if len(indv2[indx]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1]) >= selisih:
                        # print("mutasi pada index ke - 1, indv ",indx)
                        # selisih *= -1
                        selisih = -selisih
                        sdw = indv2[indx]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1]
                        # print("index ke-", selisih)
                        # print(sdw)
                        # print(sdw[selisih])
                        sdw2 = indv2[indx]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][0]
                        sdw[selisih] = random.choice(krywn)
                        tmpt = {pdhari: [sdw2, sdw]}
                        indv2[indx]['LAPAN-A2'].update(tmpt)
                    else:
                        # print("mutasi pada index ke - 0, indv ",indx)
                        sdw = indv2[indx]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][0]
                        selisih = (selisih - len(indv2[indx]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1])) * -1
                        # print("index ke-", selisih)
                        # print(sdw)
                        # print(sdw[selisih])
                        sdw[selisih] = random.choice(krywn)
                        sdw2 = indv2[indx]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1]
                        tmpt = {pdhari: [sdw, sdw2]}

                        indv2[indx]['LAPAN-A2'].update(tmpt)
                    # print("Selisih : ", batas - items)
                    # print('============================================')
                    break



    # for sdwj in indv2:
    #     print(sdwj)

    count = []
    for indv in indv2:
        ind = 0
        # print("======================== jarak per individu =====================")
        # print(indv)
    #     for s,dict in indv.items():
    #         # print(s)
    #         for h,dict in indv[s].items():
    #             bb = jb[h]
    #             for i in range(len(indv[s][h])):
    #                 # print(i)
    #                 # print(indv[s][h][i])
    #                 if len(indv[s][h][i]) != len(set(indv[s][h][i])):
    #                     ind += 2
    #                 else:
    #                     pass
    #                     # print(h," shift ke ",i," ada duplikat !")
    #                 if i == 0:
    #                     check = [i for i in indv[s][h][i] if i in indv[s][h][1]]
    #                     ind += len(check)
    #                 #
    #                 for ads in range(len(indv[s][h][i])):
    #                     # print(indv[s][h][i][ads])
    #                     # print(job_krywn[indv[s][h][i][ads]][i])
    #                     # print("jadwal harian ",bb[i])
    #                     # print("ads : ",ads)
    #                     # print("butuh sekian : ",bb[i][ads])
    #                     if bb[i][ads] in job_krywn[indv[s][h][i][ads]][i]:
    #                         pass
    #                     else:
    #                         ind += 3
    #                     # for t in range(len(bb[i])):
    #                     #     print("butuh : ",bb[i][t])
    #     count.append(ind)
    # print("Fitness : ",count)
    # print("fungsi objective after : ",sum(count))
    return indv2

    # for sdwk in hari:
    #     print(sdwk['nama_hari'])

@app.route('/ga')
def ga():
    dsjdsw = gen()
    print("print ga testtingg bismillah")
    print(dsjdsw)
    looping = 0
    eval = {}
    cross = {}

    # resp = jsonify(dsjdsw)
    # resp.status_code = 200
    ft = 1
    while(ft == 1):
        eval = evaluasi(dsjdsw)
        cross = crossover(eval)
        dsjdsw = mutasi(cross)
        count = []
        looping+=1
        for indva in range(len(dsjdsw)):
            ind = 0
            # print("======================== jarak per individu =====================")
            # print(indv)
            # print("d")
            amrullah = '11'
            tempat_amrullah = 0
            for indv in dsjdsw[indva]:

                for s, dict in indv.items():
                    # print(s)
                    for h, dict in indv[s].items():
                        bb = jb[h]
                        for i in range(len(indv[s][h])):
                            # print(i)
                            # print(indv[s][h][i])

                            if amrullah in indv[s][h][i]:
                                tempat_amrullah+=1
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

            # if tempat_amrullah != 2:
            #     tempat_amrullah -= 2
            #     if tempat_amrullah < 0:
            #         tempat_amrullah *= -1
            #         print(tempat_amrullah)
            #         ind += tempat_amrullah
            #     else:
            #         ind += tempat_amrullah
            count.append(ind)
        print("Fitness : ", count)
        print(looping)
        print("Fitness 2 : ",count)
        if count[0] == 0:
            ft = 0
        else:
            pass

        # Fitness: [8, 17, 12, 17, 16, 16]
        # 100rb 0.03 = 10
        # 200rb 0.03 = 10
        # 100rb 0.02 = 8
        # 200rb 0.02 = 9
        # 100rb 0.02 , 13 indv = 10

        #200rb 0.05 , 10 indv = 6
        #{'LAPAN-A2': {'Senin': [['6', '4', '3', '15', '21', '13', '18'], ['11', '9', '25', '23', '21', '7']], 'Selasa': [['6', '2', '4', '19', '18', '5', '23'], ['2', '10', '16', '21', '25', '13']], 'Rabu': [['6', '3', '12', '14', '15', '7', '25'], ['11', '10', '17', '21', '24', '5']], 'Kamis': [['5', '2', '4', '24', '6', '13', '22'], ['2', '9', '18', '7', '6', '25']], 'Jumat': [['6', '7', '4', '3', '15', '22', '17', '19'], ['7', '9', '8', '18', '24', '19']], 'Sabtu': [['1', '10'], ['20', '9']], 'Minggu': [['6', '10'], ['19', '9']]}}

        #menggunakan while 1 jam 50 indv 0,05% 0 fitnesss
        # 9:34 - 09:37       8 indv 0.05% 0  fitness

        # 2jam 32 menit 0.02% 8 individu 4 minggu
        #[{'LAPAN-A2': {'Senin': [['7', '4', '3', '21', '5', '23', '17'], ['1', '10', '24', '6', '20', '22']], 'Selasa': [['6', '4', '3', '21', '20', '19', '22'], ['11', '10', '18', '14', '5', '7']], 'Rabu': [['6', '4', '3', '5', '25', '16', '22'], ['11', '10', '8', '20', '15', '23']], 'Kamis': [['5', '3', '4', '17', '7', '6', '21'], ['11', '9', '13', '24', '16', '18']], 'Jumat': [['7', '5', '4', '3', '22', '15', '14', '20'], ['1', '9', '25', '6', '18', '8']], 'Sabtu': [['13', '10'], ['22', '9']], 'Minggu': [['17', '9'], ['7', '10']]}}, {'LAPAN-A2': {'Senin': [['7', '1', '12', '14', '16', '18', '25'], ['6', '10', '8', '21', '17', '20']], 'Selasa': [['7', '1', '4', '23', '22', '19', '20'], ['6', '9', '5', '21', '16', '25']], 'Rabu': [['7', '1', '12', '18', '14', '15', '16'], ['6', '9', '24', '8', '13', '21']], 'Kamis': [['6', '2', '4', '13', '16', '25', '14'], ['11', '10', '23', '19', '22', '17']], 'Jumat': [['6', '7', '2', '4', '18', '13', '5', '14'], ['11', '9', '25', '17', '19', '8']], 'Sabtu': [['25', '9'], ['7', '10']], 'Minggu': [['25', '10'], ['19', '9']]}}, {'LAPAN-A2': {'Senin': [['6', '1', '4', '18', '20', '21', '19'], ['7', '9', '8', '16', '13', '14']], 'Selasa': [['5', '1', '3', '23', '18', '16', '19'], ['11', '9', '15', '20', '8', '17']], 'Rabu': [['5', '3', '12', '21', '23', '19', '7'], ['1', '10', '24', '13', '15', '20']], 'Kamis': [['7', '3', '4', '15', '17', '22', '5'], ['11', '10', '6', '16', '18', '14']], 'Jumat': [['7', '6', '2', '12', '23', '18', '24', '21'], ['11', '10', '8', '17', '20', '13']], 'Sabtu': [['22', '10'], ['25', '9']], 'Minggu': [['20', '9'], ['22', '10']]}}, {'LAPAN-A2': {'Senin': [['5', '3', '12', '17', '16', '22', '20'], ['7', '9', '14', '21', '8', '13']], 'Selasa': [['5', '2', '12', '15', '19', '7', '23'], ['1', '9', '6', '14', '24', '13']], 'Rabu': [['6', '1', '3', '16', '14', '13', '23'], ['2', '9', '21', '18', '17', '15']], 'Kamis': [['5', '1', '3', '19', '14', '24', '23'], ['2', '9', '20', '18', '22', '8']], 'Jumat': [['5', '6', '3', '4', '25', '21', '13', '22'], ['1', '10', '24', '23', '8', '19']], 'Sabtu': [['13', '9'], ['11', '10']], 'Minggu': [['17', '9'], ['11', '10']]}}]


        #amurullah 3 jam 16 menit 0.02% 8 individu 4 minggu
        #[{'LAPAN-A2': {'Senin': [['5', '4', '12', '15', '20', '13', '17'], ['1', '10', '8', '19', '23', '22']], 'Selasa': [['7', '3', '12', '23', '17', '19', '16'], ['6', '9', '21', '13', '24', '8']], 'Rabu': [['6', '4', '3', '24', '17', '13', '22'], ['5', '9', '15', '20', '19', '18']], 'Kamis': [['5', '2', '12', '18', '15', '7', '14'], ['1', '10', '19', '23', '17', '13']], 'Jumat': [['7', '6', '4', '3', '5', '23', '25', '14'], ['2', '10', '18', '13', '15', '22']], 'Sabtu': [['1', '9'], ['24', '10']], 'Minggu': [['17', '10'], ['7', '9']]}}, {'LAPAN-A2': {'Senin': [['5', '3', '4', '19', '6', '22', '17'], ['2', '10', '14', '24', '8', '16']], 'Selasa': [['5', '1', '4', '16', '7', '6', '13'], ['2', '9', '25', '18', '15', '22']], 'Rabu': [['7', '4', '3', '19', '21', '24', '17'], ['2', '9', '16', '25', '14', '8']], 'Kamis': [['6', '3', '4', '14', '20', '13', '24'], ['5', '10', '15', '7', '22', '19']], 'Jumat': [['7', '6', '4', '12', '24', '17', '14', '5'], ['1', '10', '23', '15', '13', '21']], 'Sabtu': [['25', '9'], ['19', '10']], 'Minggu': [['13', '10'], ['8', '9']]}}, {'LAPAN-A2': {'Senin': [['5', '1', '12', '17', '15', '22', '16'], ['2', '10', '13', '8', '25', '14']], 'Selasa': [['5', '2', '3', '7', '15', '18', '17'], ['6', '9', '25', '20', '13', '21']], 'Rabu': [['5', '2', '3', '20', '13', '24', '18'], ['1', '9', '23', '19', '8', '14']], 'Kamis': [['6', '2', '4', '13', '7', '19', '5'], ['1', '10', '24', '16', '8', '17']], 'Jumat': [['7', '6', '1', '4', '17', '21', '18', '22'], ['2', '10', '5', '19', '14', '13']], 'Sabtu': [['8', '10'], ['24', '9']], 'Minggu': [['19', '10'], ['8', '9']]}}, {'LAPAN-A2': {'Senin': [['5', '2', '12', '23', '15', '21', '20'], ['1', '10', '24', '18', '17', '13']], 'Selasa': [['7', '4', '3', '19', '25', '5', '13'], ['1', '9', '18', '23', '6', '15']], 'Rabu': [['7', '2', '12', '16', '25', '14', '18'], ['1', '9', '24', '13', '20', '19']], 'Kamis': [['6', '1', '4', '24', '18', '25', '15'], ['5', '9', '16', '8', '17', '21']], 'Jumat': [['5', '6', '2', '3', '19', '21', '22', '15'], ['11', '9', '20', '25', '8', '16']], 'Sabtu': [['24', '10'], ['11', '9']], 'Minggu': [['13', '10'], ['20', '9']]}}]

        #amurullah 3 jam 16 menit 0.02% 8 individu 4 minggu (dengan codingan baru)
        #[{'LAPAN-A2': {'Senin': [['7', '2', '4', '22', '17', '15', '5'], ['6', '10', '18', '23', '16', '14']], 'Selasa': [['7', '3', '12', '5', '20', '13', '21'], ['1', '9', '14', '18', '25', '24']], 'Rabu': [['7', '2', '12', '17', '20', '14', '25'], ['5', '9', '21', '8', '18', '6']], 'Kamis': [['5', '1', '12', '13', '19', '23', '14'], ['6', '10', '7', '24', '22', '17']], 'Jumat': [['7', '6', '2', '3', '19', '21', '24', '13'], ['1', '9', '22', '25', '16', '5']], 'Sabtu': [['15', '10'], ['11', '9']], 'Minggu': [['7', '10'], ['8', '9']]}}, {'LAPAN-A2': {'Senin': [['6', '1', '3', '20', '23', '5', '25'], ['2', '10', '18', '24', '7', '22']], 'Selasa': [['5', '4', '3', '6', '7', '18', '25'], ['1', '10', '15', '14', '17', '8']], 'Rabu': [['5', '2', '12', '19', '20', '18', '16'], ['1', '10', '17', '24', '21', '23']], 'Kamis': [['6', '2', '3', '15', '24', '19', '20'], ['11', '10', '25', '23', '13', '7']], 'Jumat': [['5', '7', '1', '3', '15', '18', '23', '17'], ['2', '10', '8', '25', '24', '20']], 'Sabtu': [['19', '9'], ['6', '10']], 'Minggu': [['15', '10'], ['24', '9']]}}, {'LAPAN-A2': {'Senin': [['7', '4', '12', '25', '18', '23', '16'], ['5', '10', '19', '22', '14', '20']], 'Selasa': [['5', '4', '12', '16', '21', '19', '22'], ['7', '10', '8', '24', '20', '18']], 'Rabu': [['6', '3', '12', '13', '5', '18', '23'], ['1', '9', '7', '21', '8', '19']], 'Kamis': [['5', '2', '3', '18', '16', '13', '22'], ['6', '10', '21', '14', '17', '25']], 'Jumat': [['5', '7', '4', '3', '24', '21', '25', '20'], ['6', '9', '13', '16', '22', '17']], 'Sabtu': [['8', '9'], ['7', '10']], 'Minggu': [['8', '9'], ['25', '10']]}}, {'LAPAN-A2': {'Senin': [['5', '4', '12', '23', '16', '6', '24'], ['2', '9', '19', '13', '8', '7']], 'Selasa': [['5', '4', '12', '24', '19', '6', '23'], ['1', '9', '13', '18', '15', '17']], 'Rabu': [['5', '3', '12', '17', '6', '13', '16'], ['7', '10', '19', '22', '21', '14']], 'Kamis': [['7', '4', '3', '6', '25', '24', '21'], ['1', '10', '13', '19', '16', '23']], 'Jumat': [['7', '6', '1', '4', '16', '20', '19', '24'], ['2', '9', '17', '15', '21', '5']], 'Sabtu': [['19', '10'], ['8', '9']], 'Minggu': [['19', '9'], ['20', '10']]}}]



    print(looping)
    # print(dsjdsw)
    for wwa in dsjdsw:
        print(wwa)

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
