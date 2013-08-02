#!/usr/bin/python
# encoding: cp1251

import sys, os, urllib, urllib2, re, time, datetime, cookielib, MySQLdb

#print "По техническим причинам сервис отключен."
#sys.exit ()

datum = (datetime.datetime.now()).strftime("%d.%m.%Y")
datum_protokol = (datetime.datetime.now()+datetime.timedelta(hours=-22)).strftime("%d-%m-%y")

def anmelden():
    USERNAME = "kekus6"
    PASSWORD = "es656967"

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    urllib2.install_opener(opener)
    header = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9b4) Gecko/2008030318 Firefox/3.0b4'}
    data = urllib.urlencode({"login" : USERNAME, "pass" : PASSWORD, "LOGIN_redirect" : "1", "lreseted" : "1", "preseted" : "1"})

    request = urllib2.Request('http://www.heroeswm.ru/login.php', data, header)
    response = urllib2.urlopen(request)
    response.close()
    time.sleep(1)

def main(parameter):


    if parameter:
        klan_li = [int(parameter)]
    else:
        klan_li = [13, 14, 41, 176, 236, 464, 825, 928, 1254, 1138, 1332, 1512, 2140, 3333, 3995, 5063, 5349, 5757, 6749]

    anmelden()
    comp_zeile =re.compile(u"(?<=&nbsp;&nbsp;)(.*?)(?=<BR>)") # eine Zeile
    comp_zeile_=re.compile(u"(?<=&nbsp;&nbsp;&nbsp;)(.*?)(?=<BR>)") # eine Zeile
    comp_fett=re.compile(u"(?<=<b>)(.*?)(?=</b>)")# <b>...</b>
    comp_link = re.compile(u'(?<=\(<a href=")(.*?)(?=">)')# link
    comp_fighter=re.compile(u'(?<=<a href="pl_info.php\?id=)(.*?)(?=])') #1474677">killBASS_ko</a> [14
    comp_warid = re.compile(u'(?<=warid=)(.*?)(?=">)') # Warid
    comp_obj = re.compile(u'(?<=#)(.*?)(?=</a>)') # Object
    str_napadenie_surv = u': \u041d\u0430\u043f\u0430\u0434\u0435\u043d\u0438\u0435 \u0421\u0443\u0440\u0432\u0438\u043b\u0443\u0440\u0433\u043e\u0432' #Нападение Сурвилургов
    str_polucheno = u'\u043f\u043e\u043b\u0443\u0447\u0435\u043d\u043e '#получено
    str_proigrano = u'\u043f\u0440\u043e\u0438\u0433\u0440\u0430\u043d\u043e ' #проиграно

    db_verbindung = MySQLdb.connect ( host = "localhost", user = "d01785d8", passwd = "eYAZJLfrg9oxaopP", db = "d01785d8", charset="cp1251" )
    cursor = db_verbindung.cursor()

    for klan_num in klan_li:
        #print 'Klan:  ' + str(klan_num)
        pagecount = -1
        while True:
            break_kz = False
            pagecount += 1
            link = 'http://www.heroeswm.ru/clan_log.php?id=%d&page=%d' %(klan_num, pagecount)
            page = urllib2.urlopen(link)
            html = page.read()
            html_d = html.decode('cp1251')
            #html_d = html.decode('latin-1')
            page.close()

            zeilen = comp_zeile.findall(html_d)
            if not zeilen:
                continue

            #print zeilen[0]
            dat_tmp_str = zeilen[0][:zeilen[0].find(' ')]
            #print dat_tmp_str
            dat_tmp = datetime.datetime.strptime(dat_tmp_str, '%d-%m-%y')
            if dat_tmp < datetime.datetime(2013,06,12):
                #print 'datum ist zu klein'
                break_kz = True

            for zeile in zeilen: # schleufe ueber die zeilen im klan-protokol
                if str_napadenie_surv in zeile and str_polucheno in zeile:
                    dat_str = zeile[:zeile.find(str_napadenie_surv)]
                    dat = datetime.datetime.strptime(dat_str, '%d-%m-%y %H:%M')
                    dat_db_str = dat.strftime('%Y-%m-%d %H:%M:%S')
                    tmp_str = zeile.find('>#')+2
                    object_str = zeile[tmp_str: zeile.find('</a>', tmp_str)].replace("'", "").replace('"','')
                    tmp_str = zeile.find(' <a href="map')
                    sector_str = zeile[tmp_str: zeile.find('</a>', tmp_str)+4].replace('map.php', 'http://www.heroeswm.ru/map.php').replace('">', '" target="_blank">').replace('"','\\"')
                    tmp_str = zeile.find(str_proigrano)+13
                    proigrano_int = int(zeile[tmp_str: zeile.find('</b>', tmp_str)-1])
                    #print sector_str
                    #object_str = zeile.findall(comp_obj)
                    #print '%s,      %s' % (dat_str, object_str[:object_str.find(' ')])
                    cursor.execute('SELECT * FROM Clandef WHERE Clan_id = %d AND Obj = %s AND Datum = "%s"' % (klan_num, object_str.encode('latin-1', 'ignore'), dat_db_str))
                    all_id = cursor.fetchall()
                    if all_id:
                        break_kz = True
                        continue

                    link_ = 'http://www.heroeswm.ru/'+comp_link.findall(zeile)[0]
                    page = urllib2.urlopen(link_)
                    html = page.read()
                    html_d = html.decode('cp1251')
                    page.close()
                    zeilen_ = comp_zeile_.findall(html_d)
                    for zeile_ in zeilen_:
                        fighter_li = comp_fighter.findall(zeile_)
                        war_id = comp_warid.findall(zeile_)
                        if not war_id: continue
                        for i in fighter_li:
                            fighter_id_str = i[:i.find('"')]
                            fighter_str = i[i.find('>')+1 : i.find('<')]
                            fighter_lvl_str = i[i.find('[')+1:]
                            if str_polucheno in zeile_:
                                fighter_gold = int(fighter_lvl_str)*100
                            else:
                                fighter_gold = 0
                            #print '%s - %s' % (fighter_id_str, fighter_lvl_str)
                            if fighter_str != fighter_lvl_str:
                                cursor.execute('INSERT INTO Clandef VALUES ("%d", "%s", "%s", "%d", "%s", "%d", "%d", "%d", "%s", "%d")' \
                                 % (klan_num, dat_db_str.encode('cp1251'), object_str.encode('cp1251'), int(fighter_id_str), fighter_str.encode('cp1251'), int(fighter_gold), int(war_id[0]), int(fighter_lvl_str), sector_str.encode('cp1251'), int(proigrano_int)))
                                db_verbindung.commit()
            if break_kz:
                #print 'break'
                break


    cursor.close()
    db_verbindung.close()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        main('')
        #print 'Bitte Sklad_id angeben.'
        #sys.exit (-1)
    else:
        main(sys.argv[1])
