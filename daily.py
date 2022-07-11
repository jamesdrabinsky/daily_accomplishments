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


def update_sheet():
    client = google_client()
    sheet = client.open("Daily Accomplishments").get_worksheet(0)
    max_row = sheet.row_count
    n = next(num for num in range(1, max_row) if not sheet.row_values(num))
    sheet.update_acell(f"A{n}", f"{date.today():%Y-%m-%d}")
    sheet.update_acell(f"B{n}", list_accomplishments())


if __name__ == "__main__":
    print("\nList your daily accomplishments below:\n")
    update_sheet()
    print("\nAll done!  Thanks!\n")
