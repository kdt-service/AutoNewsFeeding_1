from konlpy.tag import Mecab
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from konlpy.tag import Kkma
import pandas as pd
from datetime import datetime,  timedelta
from summa.summarizer  import summarize
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from konlpy.corpus import kobill


def load_c_l():
    country_df = pd.read_csv('/home/ubuntu/workspace/team_1/coutry_list/country_list.csv', index_col=False)
    country_list = country_df['list'].to_list()
    return country_list

def cleansing1(df : pd.DataFrame) :
    
    """
    df : need columns name ('title', 'content')
    """

    df['content'] = df['content'].apply(lambda x : re.sub('((\(|\[).*\=.*(\]|\)).*?\= )','',str(x)))  
    df['content'] = df['content'].apply(lambda x : re.sub('\(사진=[^)]+\)','',x))
    df['content'] = df['content'].apply(lambda x : re.sub('\(현지시간\)','',x))
    df['content'] = df['content'].apply(lambda x : re.sub('\(한국시간\)','',x))
    df['content'] = df['content'].apply(lambda x : re.sub('한국시각','',x)) 
    df['content'] = df['content'].apply(lambda x : re.sub('\[|\]|\(|\)','',x))
    df['content'] = df['content'].apply(lambda x : re.sub('[가-힣A-z]+\=[가-힣A-z/0-9]+','',x))
    df['content'] = df['content'].apply(lambda x : re.sub('서울경제','',x))
    df['content'] = df['content'].apply(lambda x : re.sub('[▶△▶️◀️▷ⓒ■◆●©️▲]', '',  x))                                        
    df['content'] = df['content'].apply(lambda x : re.sub('[\xa0\u2008\u2190]', ' ',  x))
    df['content'] = df['content'].apply(lambda x : re.sub('https://', '', x))
    df['content'] = df['content'].apply(lambda x : re.sub('([\w\-]+(\@|\.)[\w\-.]+)', '',  x))
    df['content'] = df['content'].apply(lambda x : re.sub('[\.]{2,}', '.',  x))
    df['content'] = df['content'].apply(lambda x : re.sub('[\t]+', ' ',  x))
    df['content'] = df['content'].apply(lambda x : re.sub('[ ]{2,}', ' ',  x))
    df['content'] = df['content'].apply(lambda x : re.sub('[\n]{2,}', '\n',  x))
    df['content'] = df['content'].apply(lambda x : re.sub('공감언론 뉴시스가 독자 여러분의 소중한 제보를 기다립니다. 뉴스 가치나 화제성이 있다고 판단되는 사진 또는 영상을 뉴시스 사진영상부로 보내주시면 적극 반영하겠습니다.', '',  x))

    return df

def cleansing2(df) :
    """
    df : need columns name ('title', 'content')
    """

    df = df.drop(df[df['content'].str.len() <= 15].index)
    df = df.drop(df[(df['content'].str.contains('파이낸셜뉴스'))].index)
    df = df.drop(df[(df['content'].str.contains('블룸버그는'))].index)
    df = df.drop(df[(df['content'].str.contains('전진영 기자 jintonic@'))].index)
    df = df.drop(df[(df['content'].str.contains('자세한 내용 이어집니다.'))].index)
    df = df.drop(df[(df['content'].str.contains('데일리안 = 데스크 by.\n한가마'))].index)
    df.reset_index(drop=True, inplace=True)
    df.rename(columns={'content':'summa_content'}, inplace=True)
    df.drop_duplicates(subset='summa_content', inplace=True)

    return df

def summarize1(list, df):
    """
    요약본(list)를 df에 넣는 함수 \n
    news_list = df.values.tolist()
    """
    new_sum_list = [list[n][1] if summarize(list[n][1], words=15) == '' else summarize(list[n][1], words=15) for n in range(len(list))]
    df['content'] = new_sum_list

    return df

def get_words(txt):

    mecab = Mecab()

    return [t[0] for t in mecab.pos(txt) if (t[1][0] == 'N') & (len(t[0])>1)]

def get_words2(txt):

    kkma = Kkma() 

    nouns = kkma.nouns(txt) 

    return nouns

def get_country(word_list) :

    count_dict = {}
    for word in word_list:
        if word in load_c_l():
            if word == '대한민국':
                word = '한국'
            if word == '우크라':
                word = '우크라이나'
            count_dict.setdefault(word , 0)
            count_dict[word] += 1

    return count_dict

def count_country(txt1, txt2):

    words = get_words2(txt1) + get_words2(txt2)
    count = get_country(words)
    if not count:
        return []
    max(count.values())
    max_list = max(count.values()) 
    max_keys = [key for key, value in count.items() if value == max_list]

    return max_keys

def country_count(country_list):

    country_dict = {}

    for country in country_list:
        country_dict.setdefault(country, 0)
        country_dict[country] += 1
        sorted_dict = sorted(country_dict.items(), key=lambda x: x[1], reverse=True)
        
    return sorted_dict

def top_country(df_list):

    count_list = []

    for n in range(len(df_list)):
            c = count_country(df_list[n][0], df_list[n][1])
            count_list.extend(c)

    results = country_count(count_list)
    top3 = [results[0], results[1], results[2]]

    return top3

def news_dict__(df_list):
    
    news_dict = {}
    for m in range(len(df_list)):
        for country in get_country(get_words2(df_list[m][1])) :
            news_dict.setdefault(country , [])
            news_dict[country].append(df_list[m][1])
        
    return news_dict

def top_country_news(df_list):
    
    t_news_dict = {}
    top3 = top_country(df_list)
    news_dict_ = news_dict__(df_list)
    t_country = [top3[0][0], top3[1][0], top3[2][0]]
    t_news_dict[t_country[0]] = news_dict_[t_country[0]]
    t_news_dict[t_country[1]] = news_dict_[t_country[1]]
    t_news_dict[t_country[2]] = news_dict_[t_country[2]]
  
    return t_news_dict

def extract_keywords(txt):

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(txt)

    top_keywords = []
    for doc_idx in range(len(txt)):
        doc_keywords = []
        for term_idx in tfidf_matrix[doc_idx].nonzero()[1]:
            term = list(tfidf_vectorizer.vocabulary_.keys())[list(tfidf_vectorizer.vocabulary_.values()).index(term_idx)]
            if term != '':
                    doc_keywords.append((term, tfidf_matrix[doc_idx, term_idx]))
        doc_keywords = sorted(doc_keywords, key=lambda x: x[1], reverse=True)[:5]
        top_keywords.append(doc_keywords)

    return top_keywords

def keyword_list3(txt):

    keyword_list3 = []
    top_keywords = extract_keywords(txt) 

    for doc_keywords in top_keywords:
        for keyword, importance in doc_keywords:
            if importance >= 0.25 :
                keyword_list3.append(keyword)
                
    pd.Series(keyword_list3)
    results = (pd.Series(keyword_list3).value_counts()).sort_values(ascending=False)

    top3 = []
    for index, values in results.items():
        top3.append((index, values))

    return [top3[0], top3[1], top3[2]]

def summarize_news_articles(news_articles, num_summary_sentences=3):
    # 뉴스 기사들을 문장 단위로 토큰화
    sentences = []
    for news_article in news_articles:
        sentences.extend(sent_tokenize(news_article))

    # 불용어 제거 및 문장별 단어 토큰화
    word_tokens = []
    stop_words = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [word.lower() for word in words if word.isalnum()]
        words = [word for word in words if word not in stop_words]
        word_tokens.append(words)

    # 단어들의 빈도수 계산
    freq_dist = FreqDist()
    for words in word_tokens:
        freq_dist.update(words)

    # 각 문장의 중요도 계산 (TextRank 알고리즘)
    sentence_scores = {}
    for i, words in enumerate(word_tokens):
        sentence_score = 0
        for word in words:
            sentence_score += freq_dist[word]
        sentence_scores[i] = sentence_score

    # 문장의 중요도에 따라 내림차순으로 정렬
    sorted_sentence_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)

    # 상위 num_summary_sentences 개의 문장 인덱스 추출
    top_sentence_indices = [item[0] for item in sorted_sentence_scores[:num_summary_sentences]]

    # 원본 뉴스 기사의 해당 문장들 추출하여 대표기사 생성
    summary = ""
    for i in top_sentence_indices:
        summary += sentences[i] + " "

    return summary

def rep_news(list): 
    t3 = top_country_news(list)
    t3_list = top_country(list)

    one = summarize_news_articles(t3[t3_list[0][0]])
    two = summarize_news_articles(t3[t3_list[1][0]])   
    thr = summarize_news_articles(t3[t3_list[2][0]])

    return [one, two, thr]