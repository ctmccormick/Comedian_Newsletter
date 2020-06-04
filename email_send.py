import json
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import OrderedDict

today = datetime.today()

bdays_file = "wiki_data_bdays.json"
ddays_file = "wiki_data_ddays.json"
news_file = "news_dump.json"

with open(bdays_file, 'r') as f:
    bday_data = json.load(f)

with open(ddays_file, 'r') as f:
    dday_data = json.load(f)

with open(news_file, 'r') as fp:
    news_data = json.load(fp)


bdays_html = ""

ddays_html = ""

news_html = ""

browser = """<a href="http://ctmccorm.pythonanywhere.com/newsletter"><font size="2">Click here to view this email in your browser.</font></a>"""

bdays_in_order = OrderedDict(sorted(bday_data.items(), key=lambda i: i[1]['bday_this_year']))
ddays_in_order = OrderedDict(sorted(dday_data.items(), key=lambda i: i[1]['dday_this_year']))

# get list of days with events
days_with_bday = []
for k, v, in bday_data.items():
    if v['full_day'] not in days_with_bday:
        days_with_bday.append(v['full_day'])
    else:
        pass

days_with_dday = []
for k, v, in dday_data.items():
    if v['full_day'] not in days_with_dday:
        days_with_dday.append(v['full_day'])
    else:
        pass

for day in days_with_bday:
    bdays_html += "<tr><td" + """ colspan="2"> """ + "<h3>" + day + "</h3></td></tr>"
    for name, data in bdays_in_order.items():
        if data['full_day'] == day:
            bdays_html += ("<tr><td>" + "<a href=" + str(data['wiki_page']) + ">"
                           + "<img src=" + str(data['image']) + " align=left width=65 height=75 hspace=15 alt="">"
                           + "</a></td>"
                           + """<td valign="top">"""
                           + "<a href=" + data['wiki_page'] + ">" + name + " - " + str(data['age']) + "</a><br>"
                           + str(data['summary']) + "<br></td></tr>"
                           + "<tr><td> <br> </td> <td> <br> </td> </tr>")

for day in days_with_dday:
    ddays_html += "<tr><td" + """ colspan="2"> """ + "<h3>" + day + "</h3></td></tr>"
    for name, data in bdays_in_order.items():
        if data['full_day'] == day:
            ddays_html += ("<tr><td>" + "<a href=" + str(data['wiki_page']) + ">"
                           + "<img src=" + str(data['image']) + " align=left width=65 height=75 hspace=15 alt="">"
                           + "</a></td>"
                           + """<td valign="top">"""
                           + "<a href=" + data['wiki_page'] + ">" + name + " - " + str(data['age']) + "</a><br>"
                           + str(data['summary']) + "<br></td></tr>"
                           + "<tr><td> <br> </td> <td> <br> </td> </tr>")

for name, data in news_data.items():
    news_html += ("<tr><td><a href=http://" + str(data['link']) + ">" + data['title'] + "</a>"
                  + "<br>" + data['date']
                  + "<br>" + data['body']
                  + "</td></tr>")

if bdays_html == '':
    bday_table = "No birthdays this week."
else:
    pass

if ddays_html == '':
    dday_table = "No death anniversaries this week."
else:
    pass

if news_html == '':
    news_table = "No comedians in the news this week."
else:
    pass

today = datetime.today()
month_name = today.strftime("%B")
day_name = today.strftime("%A")
day_num = str(today.day)


def send_newsletter(subject, toaddr):
    fromaddr = "improvnewsfeed@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    outlook_text = """\
<!--[if gte mso 9]>
<html xmlns:v="urn:schemas-microsoft-com:vml">
    <head>
    <style>
        v:* { behavior: url(#default#VML); display: inline-block; }
    </style>
    </head>
    <body>
    <font color='white'>Hollywood Improv Comedian Newsletter</font>
    <center>
        <table width="95%" height="6px">
            <tr>
                <td bgcolor="#ffffff" style="background-image:url('https://imgur.com/dnnH4k0.jpg');background-repeat:no-repeat;background-position:center;" background="https://imgur.com/dnnH4k0.jpg" width="100%" height="90%">
                    <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="mso-width-percent:950%;height:80%;">
                        <v:fill type="frame" src="https://imgur.com/dnnH4k0.jpg" color="#ffffff" />
                    </v:rect>
                </td>
            </tr>
        </table>
    </center>
        <br>
        <div align="center">
        <a href="http://ctmccorm.pythonanywhere.com/newsletter"><font size="2">Click here to view this email in your browser.</font></a>
        </div> 
        <br>
        <h2>Comedians' Birthdays</h2>
        <table width="95%">
        <col width="80">
        """ + bdays_html + """
        </table>
        <br>
        <h2>
        Comedians in the News</h2>
        <table width="70%">
        """ + news_html + """
        </table>
        <br>
        <h2>
        Death Anniversaries</h2>
        <table width="95%">
        <col width="80">
        """ + ddays_html + """
    </table>
    </body>
    </html>
    <![endif]-->
<!--[if !mso]><!-->"""

    other_text = """
<html>
<body>
    <font color='white'>Hollywood Improv Comedian Newsletter</font><br>
    <div align="center">
    <img src='https://imgur.com/dnnH4k0.jpg' width=80%>
    </div>
    <br>
    <br>
    <div align="center">
    """ + browser + """
    </div>
    <h2>Comedians' Birthdays</h2>
     <table width="95%">
        <col width="80">
        """ + bdays_html + """
    </table>
    <h2><br><br>
    Comedians in the News</h2>
    <table width="70%">
    """ + news_html + """
    </table>
    <h2><br><br><br>
    Death Anniversaries</h2>
    <table width="95%">
        <col width="80">
        """ + ddays_html + """
    </table>
</body>    
</html>
<!--><![endif]-->
"""

    all_text = outlook_text + other_text
    msg_part = MIMEText(all_text, "html")

    msg.attach(msg_part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("improvnewsfeed@gmail.com", 'Improv1963')

    text = msg.as_string()

    server.sendmail(fromaddr, toaddr, text)
    server.quit()


daily_emails = [emails_of_daily_recipients]

weekly_emails = [emails_of_weekly_recipients]

for email in daily_emails:
    send_newsletter("Improv Newsletter - Week of " + day_name + ", " + month_name + " " + day_num, email)

if datetime.now().strftime("%A") == 'Tuesday':
    for email in weekly_emails:
        send_newsletter("Improv Newsletter - Week of " + day_name + ", " + month_name + " " + day_num, email)
