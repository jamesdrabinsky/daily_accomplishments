import argparse
from datetime import date

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def google_client() -> gspread.client.Client:
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "daily-accomplishments.json", scope
    )
    return gspread.authorize(creds)


def create_sheet(client: gspread.client.Client) -> None:
    sheet = client.create("Daily Accomplishments")
    sheet.share("james.drabinsky@gmail.com", perm_type="user", role="writer")


def list_accomplishments():
    items = []
    while True:
        item = input()
        if str(item).lower() == "stop":
            break
        else:
            items.append(str(item))
    return "\n".join(items)


def update_current_day():
    client = google_client()
    sheet = client.open("Daily Accomplishments").get_worksheet(0)
    max_row = sheet.row_count
    n = next(num for num in range(1, max_row) if not sheet.row_values(num))
    sheet.update_acell(f"A{n}", f"{date.today():%Y-%m-%d}")
    sheet.update_acell(f"B{n}", list_accomplishments())


def delete_accomplishments(target_date: str):
    client = google_client()
    sheet = client.open("Daily Accomplishments").get_worksheet(0)
    row_to_update = next(row for row, d  in enumerate(sheet.col_values(1), start=1) if d == target_date)
    sheet.update_cell(row_to_update, 2, list_accomplishments())


if __name__ == "__main__":
    print("\nList your daily accomplishments below:\n")
    update_current_day()
    print("\nAll done!  Thanks!\n")


# my_parser = argparse.ArgumentParser()
# my_parser.add_argument('action', choices=['add', 'delete'])
# args = my_parser.parse_args()
# print(args.action)
