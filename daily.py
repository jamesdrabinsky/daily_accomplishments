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


def update(action: str, target_date: str = None):
    client = google_client()
    sheet = client.open("Daily Accomplishments").get_worksheet(0)
    if not target_date:
        if action == "add":
            print("\nList today's accomplishments below:\n")
            max_row = sheet.row_count
            n = next(num for num in range(1, max_row) if not sheet.row_values(num))
            sheet.update_cell(n, 1, f"{date.today():%Y-%m-%d}")
            sheet.update_cell(n, 2, list_accomplishments())
        else: # target_date must be specified if action == "delete"
            raise Exception("A date must be specified when deleting.  Please try again.")
    else:
        n = next(
            row
            for row, d in enumerate(sheet.col_values(1), start=1)
            if d == target_date
        )
        if action == "add":
            print(f"\nAdd to your accomplishments from {target_date}:\n")
            old_text = sheet.cell(n, 2).value
            updated_text = f"{old_text}\n{list_accomplishments()}"
            sheet.update_cell(n, 2, updated_text)
        else:
            print(f"\nDeleting your accomplishments from {target_date} ...\n")
            sheet.update_cell(n, 2, "")


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument("action", choices=["add", "delete"])
    my_parser.add_argument("-dt", action="store")
    args = my_parser.parse_args()
    action, target_date = vars(args).values()
    update(action, target_date=target_date)
    print("All done!  Thanks!\n")
