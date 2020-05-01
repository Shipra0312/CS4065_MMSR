"""
This file extract videos to data_extracted folder,
Please use csgo_highlight as execution directory
"""

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import pandas as pd

metadata = pd.read_csv("data_raw/metadata.csv")
p11_metadata = metadata[metadata["perspective"] == "P11"]
p11_metadata.head()

"""
Extract Training videos for each match
"""
matches = p11_metadata[(p11_metadata["type"] == "match") & (p11_metadata["duration"] > 600)]
for i in range(0, 11):  # loop through 11 training videos
    stream_file = matches.iloc[i]["stream_file"]
    start_time = matches["start_time"].iloc[i]
    duration = matches["duration"].iloc[i]
    ffmpeg_extract_subclip("data_raw/videos/%s" % stream_file, start_time, start_time + duration,
                           "data_extracted/videos/training%d.mp4" % (i + 1))

"""
Extract Highlight videos for each match
"""

highlights = metadata[(metadata["type"] == "highlight") & (metadata["perspective"] == "P11")]
for i in range(0, 11):  # loop through 11 training videos
    match_i_df = highlights[highlights["match_id"] == i + 1]
    for row in match_i_df[["start_time", "duration", "stream_file"]].iterrows():
        start_time, duration, stream_file = row[1]
        ffmpeg_extract_subclip("data_raw/videos/%s" % stream_file, start_time, start_time + duration,
                               "data_extracted/highlights/highlight%d_%d.mp4" % (i + 1, start_time))
