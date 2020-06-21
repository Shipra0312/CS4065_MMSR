import pandas as pd

import json
import pandas as pd
from datetime import datetime

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

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
