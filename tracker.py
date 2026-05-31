import csv
import os
from datetime import date

FILE_NAME = "expenses.csv"

def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["No", "Date", "Category", "Amount", "Description"])

class ExpenseTracker:

    def add_expense(self, category, amount, description):
        today = str(date.today())
        with open(FILE_NAME, "r") as f:
            count = sum(1 for row in f) - 1
        with open(FILE_NAME, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([count + 1, today, category, amount, description])

    def get_all_expenses(self):
        with open(FILE_NAME, "r") as f:
            reader = csv.DictReader(f)
            return list(reader)

    def delete_expense(self, number):
        with open(FILE_NAME, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
        new_rows = [rows[0]]
        for row in rows[1:]:
            if row[0] != str(number):
                new_rows.append(row)
        with open(FILE_NAME, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(new_rows)