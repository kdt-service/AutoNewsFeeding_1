import smtplib
import email
import pandas as pd
from summa_ import cleansing1, cleansing2, summarize1, top_country_news, top_country, rep_news, keyword_list3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from weeky import week_of_month


news_df = pd.read_csv('test_data.csv'.format(), index_col=False) # 1주일 단위로 만들어진 파일 불러오기

c1_df = cleansing1(news_df)
c1_list = c1_df.values.tolist()
summa_list = cleansing2((summarize1(c1_list, c1_df))).values.tolist()

top_news_list = top_country_news(summa_list) # top3 기사 추출
top_country3 = top_country(summa_list) # top3 국가 추출
rep_n = rep_news(summa_list) # 대표기사 
rep_k = [keyword_list3(top_news_list[top_country3[0][0]]),keyword_list3(top_news_list[top_country3[1][0]]),keyword_list3(top_news_list[top_country3[2][0]])]
# rep_k = [[k1, k2, k3], [k1, k2, k3], [k1, k2, k3]]
print(rep_n)


# E-mail 발송

SMTP_SERVER = 'smtp.naver.com'
SMTP_PORT = 465
SMTP_USER = 'awdee14@naver.com'
SMTP_PASSWORD = open('/home/ubuntu/workspace/team_1/config/config', 'r').read().strip()

to_users = ['awdee14@naver.com']
target_addr = ','.join(to_users)

weeky = week_of_month(datetime.today())
month = datetime.today().month

subject = '{}월{}주차 세계뉴스'.format(month ,weeky)

msg = MIMEMultipart('alternative')

msg['From'] = SMTP_USER
msg['To'] = target_addr
msg['Subject'] = subject

# HTML 파일 읽어오기
with open('/home/ubuntu/workspace/team_1/html/newsletter.html', 'r', encoding='utf-8') as file:
    html = file.read()


new_week = "1"
new_country1 = top_country3[0][0]
new_country2 = top_country3[1][0]
new_country3 = top_country3[2][0]

new_keyword1_1 = rep_k[0][0][0]
new_keyword1_2 = rep_k[0][1][0]
new_keyword1_3 = rep_k[0][2][0]

new_keyword2_1 = rep_k[1][0][0]
new_keyword2_2 = rep_k[1][1][0]
new_keyword2_3 = rep_k[1][2][0]

new_keyword3_1 = rep_k[2][0][0]
new_keyword3_2 = rep_k[2][1][0]
new_keyword3_3 = rep_k[2][2][0]

new_title1_1 = "null"
new_title1_2 = "null"
new_title1_3 = "null"

new_text1_1 = rep_n[0]
new_text1_2 = "null"
new_text1_3 = "null"

new_title2_1 = "null"
new_title2_2 = "null"
new_title2_3 = "null"

new_text2_1 = rep_n[1]
new_text2_2 = "null"
new_text2_3 = "null"

new_title3_1 = "null"
new_title3_2 = "null"
new_title3_3 = "null"

new_text3_1 = rep_n[2]
new_text3_2 = "null"
new_text3_3 = "null"

formatted_html = f"{html.replace('{week}', new_week)}"
formatted_html = f"{formatted_html.replace('{country1}', new_country1).replace('{country2}', new_country2).replace('{country3}', new_country3)}"

formatted_html = f"{formatted_html.replace('{keyword1_1}', new_keyword1_1).replace('{keyword1_2}', new_keyword1_2).replace('{keyword1_3}', new_keyword1_3)}"
formatted_html = f"{formatted_html.replace('{keyword2_1}', new_keyword2_1).replace('{keyword2_2}', new_keyword2_2).replace('{keyword2_3}', new_keyword2_3)}"
formatted_html = f"{formatted_html.replace('{keyword3_1}', new_keyword3_1).replace('{keyword3_2}', new_keyword3_2).replace('{keyword3_3}', new_keyword3_3)}"

formatted_html = f"{formatted_html.replace('{title1_1}', new_title1_1).replace('{title1_2}', new_title1_2).replace('{title1_3}', new_title1_3)}"
formatted_html = f"{formatted_html.replace('{title2_1}', new_title2_1).replace('{title2_2}', new_title2_2).replace('{title2_3}', new_title2_3)}"
formatted_html = f"{formatted_html.replace('{title3_1}', new_title3_1).replace('{title3_2}', new_title3_2).replace('{title3_3}', new_title3_3)}"

formatted_html = f"{formatted_html.replace('{text1_1}', new_text1_1).replace('{text1_2}', new_text1_2).replace('{text1_3}', new_text1_3)}"
formatted_html = f"{formatted_html.replace('{text2_1}', new_text2_1).replace('{text2_2}', new_text2_2).replace('{text2_3}', new_text2_3)}"
formatted_html = f"{formatted_html.replace('{text3_1}', new_text3_1).replace('{text3_2}', new_text3_2).replace('{text3_3}', new_text3_3)}"

msg.attach(MIMEText(formatted_html, 'html'))
smtp = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
smtp.login(SMTP_USER, SMTP_PASSWORD)
smtp.sendmail(SMTP_USER, to_users, msg.as_string())
smtp.close()


