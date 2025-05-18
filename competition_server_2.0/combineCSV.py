import pandas as pd
import os

def Combine_CSV():
    CSV_Folder = 'MatchZy_Stats'
    Stat_Needed = ['steamid64', 'kills', 'deaths', 'assists', 'damage', 'head_shot_kills', 'enemy5ks', 'enemy4ks', 'enemy3ks','entry_count', 'entry_wins',
                   'utility_count', 'utility_successes', 'flash_count', 'flash_successes']
    CSV_Needed = []
    Stat = []
    
    # for root, dirs, files in os.walk(CSV_Folder):
    #     for file in files:
    #         if file.lower().endswith('.csv'):
    #             CSV_Full_Path = os.path.join(root, file)
    #             CSV_Needed.append(CSV_Full_Path)
    # 原计划：从文件夹内的文件夹中获取数据，目前只能先将文件先拖出文件夹后再进行运算

    for i in os.listdir('MatchZy_Stats'):
        if i.endswith('.csv'):
            CSV_Needed.append(i)
    
    for i in CSV_Needed:
        Tem_Stat = pd.read_csv(os.path.join(CSV_Folder, i), usecols = Stat_Needed)
        Stat.append(Tem_Stat)

    CSV_Needed = pd.DataFrame(CSV_Needed)
    Combined_CSV = pd.concat(Stat, ignore_index = True)

    Combine_Method = Combined_CSV.groupby('steamid64', as_index = False).agg({
        'kills' : 'sum',
        'deaths' : 'sum',
        'assists' : 'sum',
        'damage' : 'sum',
        'head_shot_kills' : 'sum',
        'enemy5ks' : 'sum',
        'enemy4ks' : 'sum',
        'enemy3ks' : 'sum',
        'entry_count' : 'sum',
        'entry_wins' : 'sum',

        'utility_count' : 'sum',
        'utility_successes' : 'sum',
        'flash_count' : 'sum',
        'flash_successes' : 'sum'
    })

    Combine_Method.to_csv('Player_Data.csv')

    return Combine_Method