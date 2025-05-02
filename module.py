import pandas as pd
import os
from chardet import detect

def transcode():

    Files = ('./Match_Stats')

    for filename in os.listdir('./Match_Stats'):

        if filename.endswith('.csv'):

            with open(os.path.join('./Match_Stats',filename),'rb+')as fileObj:

                fileContent = fileObj.read()

                encodingtype = detect(fileContent)['encoding']

                fileContent = fileContent.decode(encodingtype).encode('utf-8')

                fileObj.seek(0)

                fileObj.write(fileContent)
#更改编码方式

def CSV_Combining():
    original_stats = './Match_Stats'
    columns_to_keep = ['team','name','kills','deaths','assists','damage','enemy4ks','enemy5ks',
                    'flash_count','flash_successes','head_shot_kills','entry_count','entry_wins']
    files_needed = []
    stat_needed = []
    for i in os.listdir('./Match_Stats'):
        if i.endswith('.csv'):
            files_needed.append(i)
    for j in files_needed:
        temporary_stat = pd.read_csv(os.path.join(original_stats,j), usecols = columns_to_keep)
        stat_needed.append(temporary_stat)
    files_needed = pd.DataFrame(files_needed)
    combined_stat = pd.concat(stat_needed, ignore_index = True)
    processing_stat = combined_stat.groupby('name',as_index = False).agg({
        'kills':'sum',
        'head_shot_kills':'sum',
        'deaths':'sum',
        'assists':'sum',
        'damage':'sum',
        'enemy4ks':'sum',
        'enemy5ks':'sum',
        'flash_count':'sum',
        'flash_successes':'sum',
        'entry_count':'sum',
        'entry_wins':'sum'
    })
    processing_stat.to_csv('./Stats_Processed/processing_data.csv')
    stat_table = pd.read_csv('./Stats_Processed/processing_data.csv')
    return stat_table
#合并并且返回总战绩csv文件

def rating_calculating():
    df = pd.read_csv('./Stats_Processed/processing_data.csv')
    df['选手ID'] = df['name']
    df['总击杀数'] = df['kills']
    df['总死亡数'] = df['deaths']
    df['击杀死亡比'] = df.apply(lambda row: row['kills'] / row['deaths'] if row['deaths'] != 0 else 0, axis=1).round(2)
    df['总伤害'] = df['damage']
    df['总助攻数'] = df['assists']
    df['爆头击杀数'] = df['head_shot_kills']
    df['爆头率'] = df.apply(lambda row: row['head_shot_kills'] / row['kills'] if row['kills'] != 0 else 0, axis=1).round(2)
    df['尝试突破次数'] = df['entry_count']
    df['突破成功率'] = df.apply(lambda row: row['entry_wins'] / row['entry_count'] if row['entry_count'] != 0 else 0, axis=1).round(2)
    df['闪光成功率'] = df.apply(lambda row: row['flash_successes'] / row['flash_count'] if row['flash_count'] != 0 else 0, axis=1).round(2)
    df['4杀次数'] = df['enemy4ks']
    df['5杀次数'] = df['enemy5ks']
    
    df['KD占比'] = df['击杀死亡比'] * 0.93
    df['多杀占比'] = df.apply(lambda row: round((row['4杀次数'] * 4 + row['5杀次数'] * 5) / row['总击杀数'], 2) if row['总击杀数'] != 0 else 0, axis=1) 
    df['助攻占比'] = df.apply(lambda row: row['总助攻数'] / row['总击杀数'] if row['总击杀数'] != 0 else 0, axis=1).round(2) * 0.01
    df['突破占比'] = df['突破成功率'] * 0.01
    df['闪光占比'] = df['闪光成功率'] * 0.1
    df['Rating SAL'] = (df['KD占比'] + df['多杀占比'] + df['助攻占比'] + df['突破占比'] + df['闪光占比']).round(2).astype(float)
    
    df['排行'] = df['Rating SAL'].rank(ascending=False, method='min')
    df = df.sort_values(by = '排行')
    df['排行'] = df['排行'].astype(int)
    columns_order = ['排行','选手ID','Rating SAL','击杀死亡比','总击杀数','总死亡数','总助攻数','总伤害','爆头率','闪光成功率','4杀次数','5杀次数','突破成功率']
    df = df[columns_order]
    df.to_csv('./Stats_Processed/processed_data.csv',index = False)
    return df
#rating计算并生成新csv文件