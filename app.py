from module import *

import pandas as pd
from flask import Flask, render_template, request

transcode()
CSV_Combining()
rating_calculating()

app = Flask(__name__)

statsboard = pd.read_csv("./Stats_Processed/processed_data.csv")

simplified_statsboard = statsboard[['排行', '选手ID', 'Rating SAL']]

simplified_statsboard['选手ID'] = simplified_statsboard['选手ID'].apply(lambda x: f'<a href="/player/{x}">{x}</a>')

@app.route('/')
def index():
    table_html = simplified_statsboard.to_html(classes='data', header="true", index=False, escape=False)
    return render_template('index.html', table_html=table_html)

@app.route('/player/<player_id>')
def player_detail(player_id):
    player_data = statsboard[statsboard['选手ID'] == player_id].to_dict(orient='records')
    if not player_data:
        return "选手未找到", 404
    player_data = player_data[0]
    
    statsbar = ['Rating SAL','击杀死亡比', '闪光成功率', '突破成功率', '爆头率']
    
    max_values = statsboard.max(numeric_only=True)
    player_percentages = {}
    
    for key in statsbar:
        if key in player_data and key in max_values:
            player_percentages[key] = round((player_data[key] / max_values[key]) * 100, 2)
    
    return render_template('player_detail.html', player_data=player_data, player_percentages=player_percentages) 

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1988 ,debug=True)