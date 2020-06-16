import pandas as pd
from itertools import groupby
from operator import itemgetter


def extract_highlight_df(curve, threshold=0.375, min_sec_highlight=10):

    highlight_seconds = []
    for i in range(len(curve)):
        value = curve[i]
        if value >= threshold:
            highlight_seconds.append(i)

    highlight_df = pd.DataFrame(columns=['Start_time', 'End_time'])
    row_index = 0

    for k, g in groupby(enumerate(highlight_seconds), lambda x: x[0] - x[1]):
        highlights_sequence = list(map(itemgetter(1), g))
        if len(highlights_sequence) > min_sec_highlight:
            highlight_df.loc[row_index, 'Start_time'] = highlights_sequence[0]
            highlight_df.loc[row_index, 'End_time'] = highlights_sequence[-1]
            row_index = row_index + 1
