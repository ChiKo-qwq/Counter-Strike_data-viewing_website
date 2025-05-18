from combineCSV import *
from DataProcess import *
from Rating import *
from Replace64ID import *

import pandas as pd
import os, csv
from flask import Flask, render_template, request, redirect, url_for

def Refresh():
    global Steamid_Gameid_File
    global Players
    global Teams
    global Simplified_Top_Players
    global Simplified_Top_Teams
    Steamid_Gameid_File = os.path.join('Steamid_Gameid.csv')
    Players = pd.read_csv('Final_Show_Player.csv')
    Teams = pd.read_csv('Teams.csv')
    Simplified_Top_Players = Players[['排行', '选手ID', 'Rating SL']]
    Simplified_Top_Teams = Teams[['战队名', '战队积分', '战队夺冠次数', '排名']]

    Simplified_Top_Players['选手ID'] = Simplified_Top_Players['选手ID'].apply(lambda x:f'<a href = "player/{x}">{x}</a>')
    Simplified_Top_Teams['战队名'] = Simplified_Top_Teams['战队名'].apply(lambda x:f'<a href = "team/{x}">{x}</a>')

app = Flask(__name__)

try:
    Combine_CSV()
    Process_Data()
    Calculate_Rating()    
    Replace_SteamIDs()
    Refresh()
except:
    print('no such file')


@app.route('/')
#主页
def index():
    try:
        Refresh()
        Show_Top_Players = Simplified_Top_Players.to_html(classes = 'Player_Table', header = True, index = False, escape = False)
        Show_Top_Teams = Simplified_Top_Teams.to_html(classes = 'Team_Table', header = True, index = False, escape = False)

        return render_template('index.html', Show_Top_Players = Show_Top_Players, Show_Top_Teams = Show_Top_Teams)
    except:
        return render_template('Error.html')

@app.route('/player/<player_id>')
#选手详情
def Player_Data(player_id):
    try:
        Refresh()
        Player_Stat = Players[Players['选手ID'] == player_id].to_dict(orient = 'records')
        if not Player_Stat:
            return 'Player Not Found', 404
        
        Player_Stat = Player_Stat[0]

        Temp_Player_Stat = {}

        for key in ['选手ID', '排行', 'Rating SL', '总击杀数', '总死亡数', '总助攻数', '总伤害', '爆头率', '尝试突破次数', '突破成功率', '道具使用次数', '道具成功率', '闪光使用次数', '闪光成功率', '5杀次数', '4杀次数', '3杀次数']:
            if key in Player_Stat:
                Temp_Player_Stat[key] = Player_Stat[key]

        Player_Stat = Temp_Player_Stat
        
        Refresh()
        return render_template('Player_Data.html', Player_Stat = Player_Stat)
    except:
        return render_template('Error.html')

@app.route('/team/<team_id>')
#战队详情
def Team_Data(team_id):
    try:
        Refresh()
        Team_Stat = Teams[Teams['战队名'] == team_id].to_dict(orient = 'records')
        if not Team_Stat:
            return 'Team Not Found', 404
        Team_Stat = Team_Stat[0]
        Refresh()
        return render_template('Team_Data.html', Team_Stat = Team_Stat)
    except:
        return render_template('Error.html')

@app.route('/Player_SignUp', methods = ['GET', 'POST'])
#选手注册，id修改
def Player_SignUp():
    try:
        Refresh()
        if request.method == 'POST':
            Game_ID = request.form.get('Game_ID')
            Steam_ID = request.form.get('Steam_ID')

            if len(Steam_ID) != 17 or not Steam_ID.isdigit():
                return render_template('Player_SignUp.html', error = '请输入正确的Steam 64位ID(17位)')
            
            try:
                with open(Steamid_Gameid_File, 'a', newline = '') as i:
                    Writing_ID = csv.writer(i)
                    Writing_ID.writerow([Game_ID, Steam_ID])
                
                Replace_SteamIDs()
                Refresh()

                return render_template('Success.html')
            
            except Exception as e:
                return render_template('Player_SignUp.html', error = f'保存失败！原因：{str(e)}')
            
        Refresh()
        return render_template('Player_SignUp.html')
    except:
        return render_template('Error.html')

@app.route('/Team_SignUp')
#战队注册，战队修改
def Team_SignUp():
    try:
        Refresh()
        pass
        Refresh()
    except:
        return render_template('Error.html')

@app.route('/Success')
#成功界面
def Success():
    return '注册成功！'

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 1988, debug = True)