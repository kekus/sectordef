#!/usr/bin/python
# encoding: cp1251

print "Content-Type: text/html"
print ""

import cgitb; cgitb.enable()
import cgi
import urllib, urllib2, re, time, datetime, cookielib, os, MySQLdb, sys
import sectordef_db



def anmelden():
    USERNAME = "kekus4"
    PASSWORD = "es656967"

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    urllib2.install_opener(opener)
    header = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9b4) Gecko/2008030318 Firefox/3.0b4'}
    data = urllib.urlencode({"login" : USERNAME, "pass" : PASSWORD, "LOGIN_redirect" : "1", "lreseted" : "1", "preseted" : "1"})

    request = urllib2.Request('http://qrator.heroeswm.ru/login.php', data, header)
    response = urllib2.urlopen(request)
    response.close()
    time.sleep(1)

def print_form(num, dat1, dat2):
    print '''
<div id="tabs">
<ul>
<li><a href="#tabs-1">Защита предприятий</a></li>
<li><a href="#tabs-2">Инструкция</a></li>
</ul>
<div id="tabs-1">

<FORM method="post" action="index.py?result">
    '''
    print 'Номер клана: <INPUT type="text" name="Klan_id" value="%s" size="3" >' % num
    print 'Предоставить данные c:&nbsp;<INPUT id=dat type="text" name="Datum" value="%s" size="16" maxlength="16"> по <INPUT id=dat type="text" name="Datum_now" value="%s" size="16" maxlength="16">&nbsp;&nbsp;' % (dat1, dat2)
    print '''
<INPUT type="submit" value="Вывести данные" name="Send">
</FORM>

</div>
<div id="tabs-2">
<p> <b>Инструкция:</b><br>
Данный сервис открыт не для всех кланов. Условие получения доступа оговаривается через игровую личку.<br>
<br>
В поле номера клана введите номер Вашего БК.<br>
В первой таблице выведены данные за период, сгруппированные по обороняемым предприятиям.<br>
Вторая таблица предоставляет данные по каждому защитнику предприятий за учетный период.<br>
Члены клана, не участвующие в обороне предприятий, в таблице не показываются.<br>
<br>
<br>
</p>
</div>
</div>
    '''

def print_ende_leer():
    print'''<script src="jquery-1.9.1.js"></script>
<script src="jquery-ui.js"></script>
<script>

$(document).ready(function(){
    $('.accordion h2').click(function(){
  if( $(this).next().is(':hidden') )
		{
		$('.accordion h2').removeClass('active').next().slideUp();
		$(this).addClass('active').next().slideDown();
		}
return false;
	});
});
</script>

<script>
$(document).ready(function(){

 $('.info h2').click(function(){
 if( $(this).next().is(':hidden') )
  {
  $('.info h2').removeClass('active').next().slideUp();
  $(this).addClass('active').next().slideDown();
  }
  return false;
 });
});
</script>
<script>
$(function() {
/*$( "#tabs" ).tabs({event: "mouseover"});*/
$( "#tabs" ).tabs();
/*$( "#tabs" ).tabs({ heightStyle: "auto" });*/

});
</script>
</body>
</html>
        '''


def print_ende():
    spalte_sort = 2
    zeile = '</tbody>\n\
      </table>\n\
    	<div id="controls">\n\
    		<div id="perpage">\n\
    			<select onchange="sorter.size(this.value)">\n\
    			<option value="5">5</option>\n\
    				<option value="10">10</option>\n\
    				<option value="20" selected="selected">20</option>\n\
    				<option value="50">50</option>\n\
    				<option value="100">100</option>\n\
    			</select>\n\
    			<span>Колличество строк</span>\n\
    		</div>\n\
    		<div id="navigation">\n\
    			<img src="images/first.gif" width="16" height="16" alt="First Page" onclick="sorter.move(-1,true)" />\n\
    			<img src="images/previous.gif" width="16" height="16" alt="First Page" onclick="sorter.move(-1)" />\n\
    			<img src="images/next.gif" width="16" height="16" alt="First Page" onclick="sorter.move(1)" />\n\
    			<img src="images/last.gif" width="16" height="16" alt="Last Page" onclick="sorter.move(1,true)" />\n\
    		</div>\n\
    		<div id="text">Страница <span id="currentpage"></span> из <span id="pagelimit"></span></div>\n\
    	</div>\n\
    	<script type="text/javascript" src="script.js"></script>\n\
        <script src="jquery-1.9.1.js"></script>\n\
        <script src="jquery-ui.js"></script>\n\
    	<script type="text/javascript">\n\
      var sorter = new TINY.table.sorter("sorter");\n\
    	sorter.head = "head";\n\
    	sorter.asc = "asc";\n\
    	sorter.desc = "desc";\n\
    	sorter.even = "evenrow";\n\
    	sorter.odd = "oddrow";\n\
    	sorter.evensel = "evenselected";\n\
    	sorter.oddsel = "oddselected";\n\
    	sorter.paginate = true;\n\
    	sorter.currentid = "currentpage";\n\
    	sorter.limitid = "pagelimit";\n\
    	sorter.init("table",%d);\n\
      </script>\n\
<script>\n\
\n\
$(document).ready(function(){\n\
	$(".accordion h2").click(function(){\n\
	if( $(this).next().is(":hidden") )\n\
		{\n\
		$(".accordion h2").removeClass("active").next().slideUp();\n\
		$(this).addClass("active").next().slideDown();\n\
		}\n\
return false;\n\
	});\n\
});\n\
</script>\n\
\n\
<script>\n\
$(document).ready(function(){\n\
\n\
 $(".info h2").click(function(){\n\
 if( $(this).next().is(":hidden") )\n\
  {\n\
  $(".info h2").removeClass("active").next().slideUp();\n\
  $(this).addClass("active").next().slideDown();\n\
  }\n\
  return false;\n\
 });\n\
});\n\
</script>\n\
<script>\n\
$(function() {\n\
/*$( "#tabs" ).tabs({event: "mouseover"});*/\n\
$( "#tabs" ).tabs();\n\
/*$( "#tabs" ).tabs({ heightStyle: "auto" });*/\n\
\n\
});\n\
</script>\n\
    </body>\n\
    </html>' % spalte_sort
    print zeile


def main(parameter):
    print '''
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <body>
    <head>
    <meta content="text/html; charset=windows-1251" http-equiv="Content-Type" />
    <title>Защита предприятий</title>
    <link rel="stylesheet" href="jquery-ui.css" />
    <link rel="stylesheet" type="text/css" href="style_.css"/>
    </head>
    '''

    try:
        num_klan =  str(form["Klan_id"].value)
        dat_woche_str =  str(form["Datum"].value)
        temp = datetime.datetime.strptime(dat_woche_str,"%d-%m-%Y")
        dat_now_str = str(form["Datum_now"].value)
        temp = datetime.datetime.strptime(dat_now_str,"%d-%m-%Y")
    except:
        num_klan = '41'
        dat_woche_str = (datetime.datetime.now()+datetime.timedelta(seconds=7200)).strftime("%d-%m-%Y")
        dat_now_str = (datetime.datetime.now()+datetime.timedelta(seconds=7200)).strftime("%d-%m-%Y")

    print_form(num_klan, dat_woche_str, dat_now_str)

    if not parameter:
        print_ende_leer()
        return
    else:
        if form.has_key("Send"):
            db_verbindung = MySQLdb.connect ( host = "localhost", user = "d01785d8", passwd = "eYAZJLfrg9oxaopP", db = "d01785d8", charset="cp1251" )
            cursor = db_verbindung.cursor()

            anmelden()

            #klan_li = [13, 14, 41, 176, 236, 464, 825, 928, 1138, 1254, 1332, 1512, 2140, 3333, 3995, 5349, 5063, 5757, 6749]
            klan_li = [13, 41, 176, 236, 464, 825, 1138, 1254, 1332, 1512, 1535, 2140, 3333, 3995, 5063, 5349, 5757, 6749]
            klan_num = int(form["Klan_id"].value)

            fil = open('log.txt','a')
            fil.write('%s : Klan - %d, IP - %s\n' % (time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()), klan_num, os.environ['REMOTE_ADDR']))
            fil.close()

            if klan_num not in klan_li:
                print '<br>Информация по вашему клану не выдается, возможно истекла подписка. По вопросам открытия доступа обращайтесь к персонажу kekus.'
                return

            # DB aktualisieren
            sectordef_db.main(klan_num)


            if str(parameter) == 'result':
                muster_dic = {}

                # Die Datuemer festlegen
                if form.has_key("Datum"):
                    dat_form_von_str=  str(form["Datum"].value).decode('cp1251')
                else:
                    dat_form_von_str = dat_woche_str

                if form.has_key("Datum_now"):
                    dat_form_bis_str = str(form["Datum_now"].value).decode('cp1251')
                else:
                    dat_form_bis_str = dat_now_str

                try: dat_form_von = datetime.datetime.strptime(dat_form_von_str,"%d-%m-%Y")
                except ValueError:
                    dat_woche_str = datetime.datetime.now()+datetime.timedelta(seconds=7200)
                    dat_form_von = dat_woche_str
                try: dat_form_bis = datetime.datetime.strptime(dat_form_bis_str,"%d-%m-%Y")
                except ValueError:
                    dat_now_str = datetime.datetime.now()+datetime.timedelta(seconds=7200)
                    dat_form_bis = dat_now_str

                # Tabelle mit Objects
                print '''
<br><br>
<table cellpadding="0" cellspacing="0" border="0" id="table1" class="sortable">
<thead><tr><th class="nosort">№</th><th><h3>Объект</h3></th><th><h3>Сектор</h3></th><th><h3>Нападений за период</h3></th><th><h3>Выставлено защит</h3></th><th><h3>% потеряно</h3></th></tr></thead>
<tbody>
                     '''
                sql_str = 'SELECT Obj, Sector, Count(DISTINCT Datum), Count(DISTINCT War_id), Sum(DISTINCT Procent) FROM `Clandef` WHERE Date(Datum)>="%s" AND Date(Datum) <= "%s" AND Clan_id=%d GROUP BY Obj' %(dat_form_von.strftime('%Y-%m-%d'), dat_form_bis.strftime('%Y-%m-%d'), klan_num)
                cursor.execute(sql_str)
                obj_sql = cursor.fetchall()
                count = 0
                for element in obj_sql:
                    count += 1
                    obj_str = '<a href="http://www.heroeswm.ru/object-info.php?id=%d" target="_blank">%s</a>' % (int(element[0][:element[0].find(' ')]), element[0])
                    print'<tr><td> %d </td><td> %s </td><td> %s </td><td> %d </td><td> %d </td><td> %d </td></tr>' % (count, obj_str.encode('cp1251'), element[1].encode('cp1251'), int(element[2]), int(element[3]), int(element[4]) )

                print '</tbody>\n</table><br><br>\n'


                # Tebelle mit den Klanmitgliedern
                print '''
<table cellpadding="0" cellspacing="0" border="0" id="table" class="sortable">
<thead><tr><th class="nosort">№</th><th><h3>Ник</th><th><h3>Уровень</h3></th><th><h3>Золото</h3></th><th><h3>- в ресах по 180</h3></th><th><h3>- в ресах по 360</h3></th><th><h3>Защит</h3></th><th><h3>Победных защит</h3></th></tr></thead>
<tbody>
                     '''

                sql_str = 'SELECT Nick, Lvl, SUM(Gold), Count(Nick), SUM(CASE WHEN Gold > 0 THEN 1 ELSE 0 END) AS Count_win FROM `Clandef` WHERE Date(Datum)>="%s" AND Date(Datum) <= "%s" AND Clan_id=%d GROUP BY Nick' %(dat_form_von.strftime('%Y-%m-%d'), dat_form_bis.strftime('%Y-%m-%d'), klan_num)
                cursor.execute(sql_str)
                period_sql = cursor.fetchall()

                gold_sum = 0
                gold_180_sum = 0
                gold_360_sum = 0
                def_sum = 0
                win_sum = 0
                count = 0
                for element in period_sql:
                    count += 1
                    gold_sum += int(element[2])
                    gold_180_sum += int(element[2])/180
                    gold_360_sum += int(element[2])/360
                    def_sum += int(element[3])
                    win_sum += int(element[4])
                    print'<tr><td> %d </td><td> %s </td><td> %d </td><td> %d </td><td> %d </td><td> %d </td><td> %d </td><td> %d </td></tr>' %\
                         (count, element[0].encode('cp1251'), int(element[1]), int(element[2]), int(element[2])/180, int(element[2])/360, int(element[3]), int(element[4]) )
                print'<tfoot><tr><td></td><td><b>Всего:</b></td><td> - </td><td><b> %d </b></td><td><b> %d </b></td><td><b> %d </b></td><td><b> %d </b></td><td><b> %d </b></td></tr></tfoot>' %\
                      (gold_sum, gold_180_sum, gold_360_sum, def_sum, win_sum)

    print_ende()


#print "По техническим причинам сервис временно недоступен."
#sys.exit ()

form=cgi.FieldStorage()
parameter = os.getenv('QUERY_STRING')


datum = (datetime.datetime.now()).strftime("%d-%m-%Y")
dat_woche_str = (datetime.datetime.now()+datetime.timedelta(seconds=7200)).strftime("%d-%m-%Y")
dat_now_str = (datetime.datetime.now()+datetime.timedelta(seconds=7200)).strftime("%d-%m-%Y")
clan_li=['3']

if __name__ == '__main__':
    main(parameter)
