
import requests
import re
import time
import os
from config import OUTPUT_DIR
import matplotlib.pyplot as plt


def initialize(): #load CSVs/files, loads config to prep the environment
    print("initialize the program")
    if config.DEV_MODE: #print dev_mode to output depending in Config boolean value
        print("Running in Dev Mode")
    random.seed(config.SEED) #ensure consistent RNG values generated for consistent runs
    #load files, validate directories exist, connect APIs


def main(): 

    # 1. Prepare some example data
    categories = ["Cat A", "Cat B", "Cat C", "Cat D"]
    values     = [23, 17, 35, 29]

    # 2. Create the bar chart
    plt.figure(figsize=(6,4))               # width=6in, height=4in
    plt.bar(categories, values)
    plt.title("Example Category Values")
    plt.xlabel("Category")
    plt.ylabel("Value")
    plt.tight_layout()

    # 3. Ensure the output directory exists
    out_dir = "docs/images"
    os.makedirs(out_dir, exist_ok=True)

    # 4. Save the chart as a PNG
    chart_path = os.path.join(out_dir, "chart.png")
    plt.savefig(chart_path, dpi=150)        # 150 DPI for clarity
    plt.close()

    print(f"Wrote chart to {chart_path}")
if __name__ == "__main__":
    main()