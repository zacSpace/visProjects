
import requests
import re
import time
import os
#from config import OUTPUT_DIR
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd


# def initialize(): #load CSVs/files, loads config to prep the environment
#     print("initialize the program")
#     if config.DEV_MODE: #print dev_mode to output depending in Config boolean value
#         print("Running in Dev Mode")
#     random.seed(config.SEED) #ensure consistent RNG values generated for consistent runs
#     #load files, validate directories exist, connect APIs


def main(): 


    #Load Trends Data
    df = pd.read_csv('ClairObscur.csv')
    df = df.rename(columns={
        'Day': 'Date',
        'Clair Obscur: Expedition 33: (United States)': 'Trend'
    })

    # 2. (Optional) convert your Day/Date to real datetimes
    df['Date'] = pd.to_datetime(df['Date'])

    # 3. Plot with short names
    fig = px.line(df, x='Date', y='Trend', title='Clair Obscur Trends')
    fig.show()


    out_dir = "docs/images"
    os.makedirs(out_dir, exist_ok=True)

    # 4. Save the chart as a PNG
    chart_path = os.path.join(out_dir, "chart.png")
    fig.write_image(chart_path, width=800, height=600, scale=2)

    print(f"Wrote chart to {out_dir}")
if __name__ == "__main__":
    main()