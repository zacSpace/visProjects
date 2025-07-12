
import requests
import re
import time
import os
#from config import OUTPUT_DIR
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from datetime import date
from pytrends.request import TrendReq
import plotly.io as pio
from polymarket import fetch_price_history_full
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
import json

# # def initialize(): #load CSVs/files, loads config to prep the environment
# #     print("initialize the program")
# #     if config.DEV_MODE: #print dev_mode to output depending in Config boolean value
# #         print("Running in Dev Mode")
# #     random.seed(config.SEED) #ensure consistent RNG values generated for consistent runs
# #     #load files, validate directories exist, connect APIs

def run_backtest(df, pos_sd, neg_sd, hold_days, position_size, start_cash=500.0):
    """
    Expects df with a 'date' column (might be strings) plus 'zootopia' and 'Price'.
    Returns a DataFrame of portfolio value over time.
    """
    # 1) Copy & ensure 'date' is a datetime, then sort
    df_bt = df.copy()
    df_bt['date'] = pd.to_datetime(df_bt['date'], utc=True)
    df_bt = df_bt.sort_values('date').reset_index(drop=True)

    # 2) Compute 7-day change and sigma
    df_bt['lag7']  = df_bt['zootopia'].shift(7)
    df_bt['delta'] = df_bt['zootopia'] - df_bt['lag7']
    sigma = df_bt['delta'].std()

    # 3) Generate +1 / -1 signals
    df_bt['signal'] = 0
    df_bt.loc[df_bt['delta'] >=  pos_sd * sigma, 'signal'] = +1
    df_bt.loc[df_bt['delta'] <= -neg_sd * sigma, 'signal'] = -1

    # 4) Simulate portfolio
    cash      = start_cash
    positions = []
    history   = []

    for _, row in df_bt.iterrows():
        today, price, signal = row['date'], row['Price'], row['signal']

        # Open
        if signal != 0:
            units = position_size/price if signal>0 else position_size/(1-price)
            fee   = (1-price)*price*0.07 * units
            cash -= position_size + fee
            positions.append({'entry': today, 'dir': signal, 'px': price, 'units': units})

        # Close aged
        new_positions = []
        for p in positions:
            if (today - p['entry']).days >= hold_days:
                proceeds = p['units'] * (price if p['dir']>0 else (1-price))
                cash += proceeds
            else:
                new_positions.append(p)
        positions = new_positions

        # Mark-to-market
        mtm = sum(p['units'] * (price if p['dir']>0 else (1-price)) for p in positions)

        history.append({'date': today, 'value': cash + mtm})

    return pd.DataFrame(history).set_index('date')


def main(): 


    ## Pull the Pytrends data 
    pio.templates.default = "plotly"
    pytrends = TrendReq()

    search_term = "zootopia"
    start_date = "2025-02-01"
    end_date   = date.today().strftime("%Y-%m-%d")
    timeframe  = f"{start_date} {end_date}"

    pytrends.build_payload([search_term], timeframe=timeframe)
    df = pytrends.interest_over_time()
    df.index.name = "date"   # ensure the index has a name
    df = df.reset_index()    # moves the index into a real column called "date"

    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])

    df["date"] = pd.to_datetime(df["date"])

    df_full = fetch_price_history_full("49225255785153140271978028633331398187057596497890648373700315193116553934019", interval="max", fidelity=1440)
    df_full = fetch_price_history_full("49225255785153140271978028633331398187057596497890648373700315193116553934019", interval="max", fidelity=1440)
    df_full.index.name = "date"   # ensure the index has a name
    df_full = df_full.reset_index()    # moves the index into a real column called "date"
    
    ###String and merge
    df   ["day_str"] = df["date"].dt.strftime("%Y-%m-%d")
    df_full["day_str"] = df_full["date"].dt.strftime("%Y-%m-%d")

    merged = pd.merge(
        df,
        df_full,
        on="day_str",
        how="inner",
        suffixes=("_zoo","_full")
    )

    # Optionally rename day_str → date
    merged = merged.rename(columns={"day_str":"date"})
    print(merged.head())
    print(merged.columns)

    #Load Website Inputs and run the backtest
    with open("config.json") as f:
        cfg = json.load(f)
    pos_sd        = cfg["pos_sd"]
    neg_sd        = cfg["neg_sd"]
    hold_days     = cfg["hold_days"]
    position_size = cfg["position_size"]
    start_cash    = cfg.get("start_cash", 500.0)


    portfolio = run_backtest(
        merged,
        pos_sd,
        neg_sd,
        hold_days,
        position_size,
        start_cash=500.0
    )

    #Save portfolio results
    os.makedirs("docs/data", exist_ok=True)
    portfolio_path = os.path.join("docs/data", "portfolio.csv")
    portfolio.to_csv(portfolio_path)
    print(f"Wrote portfolio CSV to {portfolio_path}")

    eqfig = px.line(
        portfolio.reset_index(),
        x="date",
        y="value",
        title="Portfolio Value Over Time",
    )
    eq_out = os.path.join("docs/images", "portfolio.png")
    eqfig.write_image(eq_out, engine="kaleido")
    print(f"Wrote equity curve to {eq_out}")


    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 2) Add the Zootopia trace on the primary y-axis
    fig.add_trace(
        go.Scatter(
            x=merged["date"],
            y=merged["zootopia"],
            name="Zootopia Searches",
            mode="lines+markers"
        ),
        secondary_y=False
    )

    # 3) Add the Price trace on the secondary y-axis
    fig.add_trace(
        go.Scatter(
            x=merged["date"],
            y=merged["Price"],
            name="Market Price",
            mode="lines+markers"
        ),
        secondary_y=True
    )

    # 4) Update titles and axis labels
    fig.update_layout(
        title=f"Zootopia Searches vs. Market Price ({start_date} to {end_date})",
        xaxis_title="Date"
    )
    fig.update_yaxes(title_text="Zootopia Search Trend", secondary_y=False)
    fig.update_yaxes(title_text="ZooTopia 'Yes' Market Price",           secondary_y=True)

    # 5) Save and show
    out_dir = "docs/images"
    os.makedirs(out_dir, exist_ok=True)
    chart_path = os.path.join(out_dir, "chart.png")
    fig.write_image(chart_path, engine="kaleido")
    fig.show()
    print(f"Wrote chart to {chart_path}")






if __name__ == "__main__":
    main()