import csv
import os
import datetime

FILE_NAME = "trade_analytics.csv"

def log_decision(decision_data):
    # decision_data هو قاموس (dictionary) يحتوي على كافة التفاصيل
    file_exists = os.path.isfile(FILE_NAME)
    
    with open(FILE_NAME, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=decision_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(decision_data)
