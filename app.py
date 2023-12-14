import pandas as pd
from nba_api.stats.endpoints import scoreboard
from flask import Flask, render_template

standings = scoreboard.Scoreboard(game_date='2023-12-13')

east_conf_standings_data = standings.get_data_frames()[4]
west_conf_standings_data = standings.get_data_frames()[5]

east_conf_standings_json = east_conf_standings_data.to_json(orient='records')
west_conf_standings_json = west_conf_standings_data.to_json(orient='records')

app = Flask(__name__)

@app.route('/')
def index():
    # Pass the JSON data to the HTML template
    return render_template('isl-nba-main.html', east_conf_standings_json=east_conf_standings_json, west_conf_standings_json=west_conf_standings_json)

if __name__ == '__main__':
    app.run()

