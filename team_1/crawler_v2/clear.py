from datetime import datetime, timedelta
import pandas as pd


def clear_data():
    file_path = '/home/ubuntu/workspace/team_1/new_data/weekly_news_data.csv'

    a = pd.read_csv(file_path)
    today = datetime.today().date()
    a['writed_at'] = pd.to_datetime(a['writed_at'])
    a = a.loc[a['writed_at'] >= today]
    
    return a.to_csv(file_path)
