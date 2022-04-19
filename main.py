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
            bbb = {}
            for sat in satelit:
                s = sat['nama_satelit']
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

        # ------------------------ for DEBUGING ---------------------- #
        for i in indv2:
            print(i)


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
    for indv in indv2:
        ind = 0
        # print("======================== jarak per individu =====================")
        # print(indv)
        for s,dict in indv.items():
            # print(s)
            for h,dict in indv[s].items():
                bb = jb[h]
                for i in range(len(indv[s][h])):
                    # print(i)
                    # print(indv[s][h][i])
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
        count.append(ind)
    print("Fitness : ",count)
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
    # print("Urutan : ",tmmm)

    indv3 = copy.deepcopy(indv2)

    for i in range(len(tmmm)):
        indv2[i] = copy.deepcopy(indv3[tmmm[i]])
    # print(indv3)
    # print(indv2)

    # print("Setelah Seleksi:")
    # for jkl in indv2:
    #     print(jkl)

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

    print("Individu yang akan di CROSSOVER ( tmept ) :")
    print(tmept)

    ackw = 0
    acka = 0
    for indv in indv2:
        #============ satelit permanen 2 ===============#
        for s,dict in indv.items():
            acka = int (len(indv[s]))
            # ackw = int (len(indv[s])*2)
            ackw = int(len(indv[s]))
            break
        break

    tm2 = []
    # print("testing liat individu")

    # print("")

    for v in tmept:
        ajks = copy.deepcopy(indv2[v])
        tm2.append(copy.deepcopy(ajks))
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


    for bv in range(len(tm2)):
        pj = int(len(tm2))
        # print("Jika ",(bv+1)," < ",pj)
        if ((bv+1)<pj):
            mmbc = acakArr[bv]
            bc = mmbc/acka

            kl = mmbc
            tt = kl
            for cc in range(acka-mmbc):
                h = hari[tt]
                # print(h)
                hri = (h['nama_hari'])
                tempat = (tm2[bv +1]['LAPAN-A2'][hri]).copy()
                dd[bv]['LAPAN-A2'][hri] = tempat.copy()
                tt += 1
                # print("kesatu")
            # print("")
        else:
            mmbc = acakArr[bv]
            bc = mmbc / acka
            kl = mmbc
            tt = kl
            for cc in range(acka - mmbc):
                h = hari[tt]
                # print(h)
                hri = (h['nama_hari'])
                tempat = (tm2[0]['LAPAN-A2'][hri]).copy()
                dd[bv]['LAPAN-A2'][hri] = tempat.copy()
                tt += 1
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

    #Menghitung total gen x populasi
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
    #================Generate random posisi===============
    acakMut = []
    for acak in range(math.floor(jum*0.05)):
        ct = random.randint((juml+1), jum)
        while ct in acakMut:
            ct = random.randint((juml+1), jum)
        acakMut.append(ct)

    # print(acakMut)

    #====== ambil berapa jumlah per hari lalu dimasukkan ke ARRAY ====#
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
    print(totalGen)
    print(hari_k)
    print("Total gen : ",totalGen)

    #==================== MAIN MUTASI ==============#

    for itm in acakMut:
        tm = itm / (totalGen+1)
        #Jika random number dibawah 74 ( jumlah gen individu )
        if (tm <= 1):
            for batas in hari_k:
                # print(batas)
                if batas>=itm:
                    selisih = batas - itm
                    # print(hari_k.index(batas))
                    pdhari = hari[hari_k.index(batas)]['nama_hari']
                    # print(pdhari)

                    if len(indv2[0]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1])>= selisih:
                        # print("mutasi pada index ke - 1")
                        # selisih *= -1
                        selisih = -selisih
                        sdw = indv2[0]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1]
                        # print(sdw)
                        # print(sdw[selisih])
                        sdw2 = indv2[0]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][0]
                        sdw[selisih] = random.choice(krywn)
                        tmpt = {pdhari:[sdw2,sdw]}
                        indv2[0]['LAPAN-A2'].update(tmpt)
                    else:

                        # print("mutasi pada index ke - 0")
                        sdw = indv2[0]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][0]
                        selisih = (selisih - len(indv2[0]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1]))*-1
                        # print(sdw)
                        # print(sdw[selisih])
                        sdw[selisih] = random.choice(krywn)
                        sdw2 = indv2[0]['LAPAN-A2'][hari[hari_k.index(batas)]['nama_hari']][1]
                        tmpt = {pdhari:[sdw,sdw2]}
                        indv2[0]['LAPAN-A2'].update(tmpt)

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
                        print("kapan kesininya")
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
        for indv in dsjdsw:
            ind = 0
            for s, dict in indv.items():
                for h, dict in indv[s].items():
                    bb = jb[h]
                    for i in range(len(indv[s][h])):
                        if len(indv[s][h][i]) != len(set(indv[s][h][i])):
                            ind += 2
                        else:
                            pass
                        if i == 0:
                            check = [i for i in indv[s][h][i] if i in indv[s][h][1]]
                            ind += len(check)
                        for ads in range(len(indv[s][h][i])):
                            if bb[i][ads] in job_krywn[indv[s][h][i][ads]][i]:
                                pass
                            else:
                                ind += 3
            count.append(ind)
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



    print(looping)
    # print(dsjdsw)
    for wwa in dsjdsw:
        print(wwa)

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
    app.run()
