import pandas as pd
import os

folder_path = "../football_data/premier-league"

csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

combined_df = pd.DataFrame()

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path)
    df['SourceFile'] = file  
    combined_df = pd.concat([combined_df, df], ignore_index=True)

combined_df.to_csv("premier_league.csv", index=False)


