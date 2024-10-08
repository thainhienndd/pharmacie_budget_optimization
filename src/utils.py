import pandas as pd


def add_new_df_line(df, dict_new_line):
    new_line = pd.DataFrame(data=dict_new_line)
    updated_df = pd.concat([df, new_line])
    return updated_df

