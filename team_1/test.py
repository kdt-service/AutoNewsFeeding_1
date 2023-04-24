import datetime

# 현재 시간을 문자열로 반환하는 함수
def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 현재 시간을 파일에 쓰는 함수
def write_current_time_to_file():
    with open('/home/ubuntu/workspace/team_1/current_time.txt', 'a') as file:
        current_time = get_current_time()
        file.write(current_time + '\n')


write_current_time_to_file()