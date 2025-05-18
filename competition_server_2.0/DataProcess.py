import pandas as pd

def Process_Data():
    Stat = pd.read_csv('Player_Data.csv')

    Stat['总击杀数'] = Stat['kills']
    Stat['总死亡数'] = Stat['deaths']
    Stat['总助攻数'] = Stat['assists']
    Stat['总伤害'] = Stat['damage']
    Stat['爆头击杀数'] = Stat['head_shot_kills']
    Stat['5杀次数'] = Stat['enemy5ks']
    Stat['4杀次数'] = Stat['enemy4ks']
    Stat['3杀次数'] = Stat['enemy3ks']
    Stat['尝试突破次数'] = Stat['entry_count']
    Stat['突破成功次数'] = Stat['entry_wins']

    Stat['道具使用次数'] = Stat['utility_count']
    Stat['道具有效次数'] = Stat['utility_successes']
    Stat['闪光使用次数'] = Stat['flash_count']
    Stat['闪光有效次数'] = Stat['flash_successes']

    Stat['击杀死亡比'] = Stat.apply(lambda row: row['kills'] / row['deaths'] if row['deaths'] != 0 else 0, axis=1).round(2)
    Stat['突破成功率'] = Stat.apply(lambda row: row['entry_wins'] / row['entry_count'] if row['entry_count'] != 0 else 0, axis=1).round(2)
    Stat['道具成功率'] = Stat.apply(lambda row: row['utility_successes'] / row['utility_count'] if row['utility_count'] != 0 else 0, axis=1).round(2)
    Stat['闪光成功率'] = Stat.apply(lambda row: row['flash_successes'] / row['flash_count'] if row['flash_count'] != 0 else 0, axis=1).round(2)
    Stat['爆头率'] = Stat.apply(lambda row: row['head_shot_kills'] / row['kills'] if row['kills'] != 0 else 0, axis=1).round(2)

    Stat.drop(Stat[(Stat.kills == 0) & (Stat.deaths == 0) & (Stat.damage == 0)].index, inplace = True)

    Stat.to_csv('Player_Data.csv')
    return Stat