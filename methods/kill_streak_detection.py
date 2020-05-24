import json
import pandas as pd
from datetime import datetime

timeline_df = pd.read_json("data_raw/timelines/1.json")
timeline_df["date"] = timeline_df["date"]

# get start_time in meta_data.csv
metadata_df = pd.read_csv("data_raw/metadata.csv")
start_time = metadata_df[(metadata_df["type"] == "match") &
                         (metadata_df["perspective"] == "P11") &
                         (metadata_df["match_id"] == 1)]["UTC_timestamp"]

template = "%Y-%m-%d %H:%M:%S"
start_time = datetime.strptime(start_time.iloc[0][:19], template)  # leave out +00:00

rounds = timeline_df["roundIdx"].max()

# Construct DataFrame with only kill info

kills = []
for i in range(1, rounds + 1):
    round_info = timeline_df[timeline_df["roundIdx"] == i]
    round_kill_info = round_info[round_info["type"] == "kill"]

    # get killer and victim for every kill in the round
    for row in round_kill_info.iterrows():
        data_dict = row[1].to_dict()["data"]

        killer = data_dict["actor"]["playerId"]
        killer_team = data_dict["actor"]["ingameTeam"]
        victim = data_dict["victim"]["playerId"]
        victim_team = data_dict["victim"]["ingameTeam"]
        video_second = (row[1].to_dict()["date"] - start_time).total_seconds()
        kills.append([i, killer, killer_team, victim, victim_team, video_second])

kill_df = pd.DataFrame(kills, columns=["round", "killer", "killer_team", "victim", "victim_team", "video_second"])

# get rounds where all kills are conducted within 10 seconds.
highlights1 = []
for i in range(1, rounds + 1):
    round_info = kill_df[kill_df["round"] == i]
    for team in ["CT", "TERRORIST"]:
        team_kill_info = round_info[round_info["killer_team"] == team]
        if len(team_kill_info) > 4:
            first_kill_sec = team_kill_info["video_second"].min()
            last_kill_sec = team_kill_info["video_second"].max()
            kill_duration = last_kill_sec - first_kill_sec
            if kill_duration < 10:
                highlights1.append((first_kill_sec, last_kill_sec))


