import pandas as pd

def Calculate_Rating():
    Stat = pd.read_csv('Player_Data.csv')

    Stat['KD_Precentage'] = Stat['击杀死亡比'] * 0.93
    Stat['Multi-Kill_Precentage'] = (Stat['5杀次数'] + Stat['4杀次数'] + Stat['3杀次数']) / Stat['总击杀数']
    Stat['Assist_Percentage'] = (Stat['总助攻数'] / Stat['总击杀数']) * 0.01
    Stat['Entry_Percentage'] = Stat['突破成功率'] * 0.01
    Stat['Utility_Percentage'] = Stat['道具成功率'] * 0.03 + Stat['闪光成功率'] * 0.07
    Stat['Rating SL'] = (Stat['KD_Precentage'] + Stat['Multi-Kill_Precentage'] + Stat['Assist_Percentage'] + 
                        Stat['Entry_Percentage'] + Stat['Utility_Percentage']).round(2).astype(float)

    Stat['排行'] = Stat['Rating SL'].rank(ascending = False, method = 'min').astype(int)
    Stat = Stat.sort_values(by = '排行')
    
    Stat_Kept = ['排行', 'steamid64', 'Rating SL', '总击杀数', '总死亡数', '总助攻数', '总伤害',
                 '爆头率', '尝试突破次数', '突破成功率', '5杀次数', '4杀次数', '3杀次数',
                 '道具使用次数', '道具成功率', '闪光使用次数', '闪光成功率']
    Stat = Stat[Stat_Kept]

    Stat.to_csv('Player_Data.csv')
    Stat.to_csv('Final_Show_Player.csv')

    return Stat