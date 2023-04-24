# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import pandas as pd
import os
import re

DATE_DIR = '/home/ubuntu/workspace/team_1/crawler_v2/crawl_config/date'
URL_DIR = '/home/ubuntu/workspace/team_1/crawler_v2/crawl_config/last_urls'

last_date = open(DATE_DIR, 'r').read()
last_date = datetime.strptime(last_date, '%Y-%m-%d')
date_today = datetime.now()

subcat_id = ['231', '232', '233', '234', '322']
subcat_dict = {
    '231': '아시아/호주',
    '232': '미국/중남미',
    '233': '유럽',
    '234': '중동/아프리카',
    '322': '세계일반'
}


# 마지막으로 크롤링한 url을 로그파일에 저장
def save_first_crawled_url(subcat_id, url, path):
    last_urls = read_last_url(path)
    last_urls[subcat_id] = url
    with open(path, 'w') as f:
        json.dump(last_urls, f)


# url 로그파일 읽어오기
def read_last_url(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}


def get_urls():

    new_urls_list = []
    last_urls = read_last_url(URL_DIR)

    last_dates = datetime.strptime(open(DATE_DIR, 'r').read(), '%Y-%m-%d')


    for sub_cat, name in subcat_dict.items():

        print('==========================================================================================')
        print(' > sub_cat : ', sub_cat)
        print(' > name : ', name)
        print('\n')
        
        # 마지막 크롤링 일자보다 이후 일자만 수집하기
        date_range = (date_today - last_dates).days + 1
        date_range = range(date_range) if date_range > 0 else [0]
        # [0]리스트를 사용하여 last_date와 date_today가 같은 경우에도 마지막으로 크롤링한 페이지를 다시 수집하지 않고 건너뜀

        for day in date_range:
            target_date = (last_dates + timedelta(days=day)).strftime('%Y%m%d')
            page = 1
            prev_link = None
            print('현재 날짜:', target_date)

            cnt = 0                # 첫번째 기사를 추출하기 위한 카운트
            first_url = None       # 첫번째 기사를 임시로 저장하는 변수

            # 네이버 하위 카테고리 안을 무한으로 돌면서, 기사 크롤링하기
            while True:
                BASE_URL = f'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={sub_cat}&sid1=104&date={target_date}&page={page}'
                res = requests.get(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(res.text, 'html.parser')
                print('현재 페이지:', page)


                # 해당 페이지의 첫번째 링크와 이전 페이지의 첫번째 링크가 같을 때 break
                first_link = soup.select_one('#main_content dt[class!=photo] a[href]')
                if first_link['href'] == prev_link:
                    print(' - [break] 더이상 페이지가 없습니다. ')
                    break

                # 해당 페이지의 모든 링크 리스트에 저장
                elements = soup.select('#main_content dt[class!=photo] a[href]')
                for urls in elements:
                    print(cnt, '번째 기사')
                    only_url = urls['href']

                    # 하위 카테고리에서 가장 최신의 첫번째 기사를 last
                    if cnt == 0 :
                        first_url = only_url
                        print(' - 첫번째 기사 업데이트 : ', urls)

                    # 이전에 크롤링한 URL과 현재 수집한 URL이 같으면 루프 빠져나가기
                    if only_url == last_urls.get(sub_cat):
                        print(' - [break] 현재 URL이 last_urls와 동일', only_url)
                        break

                    new_urls_list.append(only_url)
                    cnt += 1
                        
                # 이전에 크롤링한 URL과 현재 수집한 URL이 같으면 카테고리 루프 빠져나가기(종료)
                if only_url == last_urls.get(sub_cat):
                    print(' - [break] 현재 URL이 last_urls와 동일로 페이지 탐색 종료')
                    last_urls[sub_cat] = first_url       # 반복문 종료될 때, 첫번째 기사로 업데이트

                    # 크롤링한 url 저장
                    with open(URL_DIR, 'w') as f:
                        json.dump(last_urls, f)

                    # 날짜 최신화
                    with open(DATE_DIR, 'w') as f:
                        f.write(date_today.strftime('%Y-%m-%d'))

                    break
                
                prev_link = first_link['href']
                page += 1

        print('==========================================================================================\n\n\n')


    return new_urls_list



def cleansing_content(text:str):
    # 특수기호 제거
    text = re.sub('[▶△▶️◀️▷ⓒ■◆●©️]', '', text)
    # ·ㆍ■◆△▷▶▼�"'…※↑↓▲☞ⓒ⅔
    
    text = text.replace('“','"').replace('”','"')
    text = text.replace("‘","'").replace("’","'")

    # 인코딩오류 해결 (공백으로 치환)
    text = re.sub('[\xa0\u2008\u2190]', ' ', text)

    # URL제거를 위해 필요없는 문구 처리
    text = text.replace('https://', '')
    # 이메일 처리, URL 제거
    # '[\w\.-]+(\@|\.)[\w\.-]+\.[\w\.]+'
    text = re.sub('([\w\-]+(\@|\.)[\w\-.]+)', '', text)
    # ., 공백, 줄바꿈 여러개 제거 
    # \s -> 공백( ), 탭(\t), 줄바꿈(\n)
    text = re.sub('[\.]{2,}', '.', text)
    text = re.sub('[\t]+', ' ', text)
    text = re.sub('[ ]{2,}', ' ', text)
    text = re.sub('[\n]{2,}', '\n', text)

    return text

### 뉴스기사 상세 정보 크롤링 ###
def parse_news():

    new_urls_list = get_urls()
    news_list = []

    # 기사가 없을 경우
    if len(new_urls_list) == 0:
        print('신규 기사가 없습니다')
        return ''
    
    # 기사가 있을 경우
    for url in new_urls_list:
        try: 
            URL = url
            res = requests.get(URL, headers={'User-Agent':'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'html.parser')

            title = soup.select_one('#title_area.media_end_head_headline span').text.strip()
            content = ''.join(soup.select_one('#dic_area').text.strip()).replace('\n', '')
            writed_at = soup.select('.media_end_head_info_datestamp_bunch span[data-date-time]')[0].get('data-date-time')


            NaverNewsData = {
                'title' : title,
                'content' : content,
                'writed_at' : writed_at
            }

            news_list.append(NaverNewsData)

        # css 셀렉터가 안 먹히는 기사가 있음 
        except:
            pass 

    new_contents_df = pd.DataFrame(news_list)
    new_contents_df['content'] = new_contents_df['content'].apply(cleansing_content)

    return new_contents_df


def load_crawled_contents(file_path):
    try:
        news = pd.read_csv(file_path, index_col=False)
        return news
    except:
        return pd.DataFrame()


def save_news_data(file_path, old, new):
    
    data = pd.concat([old,new])
    
    data.to_csv(file_path, index=False)




if __name__ == '__main__':

    last_date = open(DATE_DIR, 'r').read()
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    date_today = datetime.now()

    new_contents = parse_news()

    # start_date_str = (datetime.now() - timedelta(days=6)).strftime('%m-%d')
    # end_date_str = date_today.strftime('%m-%d')
    # file_name = f'news_data_{start_date_str}_{end_date_str}.csv'
    file_name = 'weekly_news_data.csv'
    file_path = os.path.join('/home/ubuntu/workspace/team_1/new_data/', file_name)

    crawled_contents = load_crawled_contents(file_path)
    save_news_data(file_path, crawled_contents, new_contents)

