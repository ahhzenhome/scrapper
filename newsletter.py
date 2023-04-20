import smtplib
import credential
from datetime import datetime
from email.message import EmailMessage
from string import Template
from pathlib import Path

path_item = [Path().home(), "project", "scrapper", "news_template.html"]
li = "<li><h3>LISTITEM</h3></li>"
def populate_template(news_data):
    todaynow = datetime.now().strftime("%d/%m/%Y %X")
    section = ""
    news_li_html = ""
    for item in news_data:
	#if section != item.get("section"):
	#   section = item.get("section")
	#   section_item = f"<h2> {section} </h2>"
	#   news_li_html += section_item
        news_url = item.get("url")
        news_title = item.get("title")
        news_age = item.get("age")
        news_score = item.get("score")
        # news_item = f"<a href='{news_url}'>{news_title}</a>"
        news_item = f"<h3><a href='{news_url}'>{news_title}</a>" + f" ({news_age})" + f" rating: {news_score}</h3>"
        listitem = li.replace("LISTITEM", news_item)
        news_li_html += listitem

    news_detail = {"datetime": todaynow, "news_list": news_li_html}
    path_template = ""
    for item in path_item:
        path_template = Path(path_template, item)
    print(f"Opening template file : {path_template}")
    news_template = Template(path_template.read_text())
    news_template = news_template.substitute(news_detail)
    return news_template

def send_email(news_data):

	email = EmailMessage()
	email["from"] = "Pizen"
	email["to"] = os.getenv("MAIL_LIST").split(":")
	email["subject"] = "Hacker News NOW!"

	news_template = populate_template(news_data)
	email.set_content(news_template,"HTML")

	with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
	    smtp.ehlo()
	    smtp.starttls()
	    smtp.login(credential.username, credential.password)
	    smtp.send_message(email)
	    print("Daily News Letter is Sent")
