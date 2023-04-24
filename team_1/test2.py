from konlpy.tag import Kkma



def get_words2(txt):

    kkma = Kkma() 

    nouns = kkma.nouns(txt) 

    return nouns

print(get_words2("한편 EU 회원국 대사들은 5일 논의에서 벨라루스에 대한 제재 확대도 논의할 것으로 전해졌다 미국"))