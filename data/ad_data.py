import pandas as pd
import json, datetime

# Load datasets
ad_csv = pd.read_csv("data\\video-ad-exhibitions.csv", sep='\t')
ad_csv = ad_csv.drop(['watch_id'], axis=1)

def date_to_time(date):
    time = date.split('T')[1].strip('Z').split('.')[0].split(':')
    return int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])

def duration_to_seconds(dur):
    dur = dur.split('PT')[1]
    seconds = 0

    if 'H' in dur:
        seconds += int(dur.split('H')[0]) * 3600
        dur = dur.split('H')[1]

    if 'M' in dur:
        seconds += int(dur.split('M')[0]) * 60
        dur = dur.split('M')[1]

    if 'S' in dur:
        seconds += int(dur.split('S')[0])

    return seconds


data = json.load(open('data\\ads-api.json', 'r'))
ad_json = pd.DataFrame(data.values(), index=data.keys()).drop(['description', 'title'], axis=1)
ad_json.reset_index(inplace=True)
ad_json.rename(columns={'index': 'ad_id'}, inplace=True)
ad_json['publishedAt'] = ad_json['publishedAt'].apply(date_to_time)
ad_json['duration'] = ad_json['duration'].apply(duration_to_seconds)

# Merge datasets
ad_info = pd.merge(ad_csv, ad_json, on="ad_id")
ad_info['skip_dur'] = ad_info['skip_dur'].fillna(ad_info['duration'])

# Group by ad_id, take the mean of skip_dur
avg_skip_dur = ad_info.groupby('ad_id')['skip_dur'].mean().reset_index()
ad_info = ad_info.drop(['skip_dur'], axis=1).groupby('ad_id').first().reset_index()
ad_info = pd.merge(ad_info, avg_skip_dur, on="ad_id")
ad_info['retention'] = ad_info['skip_dur'] / ad_info['duration']
ad_info.drop(['duration', 'skip_dur'], axis=1, inplace=True)

# Save the dataset
ad_info.to_csv('data\\ad_info.csv', index=False)

print(ad_info)