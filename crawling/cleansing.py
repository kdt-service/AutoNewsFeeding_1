import re

def cleasning(df) :
    for i in range(len(df)):
        regex_parenthesis_1 = '[({[<].%s.?[)}]>]'%(df['writer'][i]) # 기자명
        regex_parenthesis_2 = '[({[<].%s.?[)}]>]'%(df['source'][i]) # 언론사명
        regex_clean = ".*\= |\(.*\=.*\)|\[.*\]|\<.*\>|.+\d{1,}\.\d{1,}\.\d{1,}\/.+|\(\▶.+\)|.+\ⓒ.+|\*.+|.+[\w._%+-]+\@[\w.-]+\.[\w]{2,}.+|.+[\w]+\.[\w.-]+..+"

        test = re.sub(regex_parenthesis_1, '', df['content'][i])
        test = re.sub(regex_parenthesis_2, '', df['content'][i])
        test = re.sub(regex_clean, '', df['content'][i])
        test = test.split('\n')
        new = []
        for text in test:
            if df['writer'][i] not in text:
                if df['source'][i] not in text:
                    new.append(text)

        new = ' '.join(str(s) for s in new)
        new = ' '.join(str(s) for s in new.split())

        # print(new)
    return new 

# cleansing thanks to 승석