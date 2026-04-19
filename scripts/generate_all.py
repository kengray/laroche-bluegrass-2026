# =============================================================================
# generate_all.py
# Reads data/schedule.json and generates:
#   - LaRoche2026.ics  (subscribable calendar file)
#   - LaRoche2026_Festival_Schedule.xlsx  (formatted spreadsheet)
#
# Run locally:  python generate_all.py
# In CI:        triggered automatically by GitHub Actions on push to schedule.json
#
# Requires: openpyxl  (pip install openpyxl)
# =============================================================================

import json
from datetime import datetime, timedelta
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# Load schedule data from JSON
# ---------------------------------------------------------------------------
data_path = Path(__file__).parent / "data" / "schedule.json"
with open(data_path, encoding="utf-8") as f:
    data = json.load(f)

FESTIVAL_LOCATION  = data["festival"]["location"]
CAMP_LOCATION      = data["festival"]["camp_location"]
FESTIVAL_NAME      = data["festival"]["name"]

# ---------------------------------------------------------------------------
# Date lookup: display string -> DD/MM/YYYY
# ---------------------------------------------------------------------------
DATE_MAP = {
    "Mon 27 Jul": "27/07/2026",
    "Tue 28 Jul": "28/07/2026",
    "Wed 29 Jul": "29/07/2026",
    "Thu 30 Jul": "30/07/2026",
    "Fri 31 Jul": "31/07/2026",
    "Sat 1 Aug":  "01/08/2026",
    "Sun 2 Aug":  "02/08/2026",
}

# =============================================================================
# ICS GENERATION
# =============================================================================

def make_ics_event(uid, summary, date_str, start_time, end_time, description, location):
    """Build a single VEVENT block. Handles acts that finish past midnight."""
    date     = datetime.strptime(date_str, "%d/%m/%Y")
    sh, sm   = int(start_time[:2]), int(start_time[3:])
    eh, em   = int(end_time[:2]),   int(end_time[3:])
    start_dt = date.replace(hour=sh, minute=sm)
    end_dt   = date.replace(hour=eh, minute=em)
    if end_dt <= start_dt:          # crosses midnight
        end_dt += timedelta(days=1)
    fmt  = "%Y%m%dT%H%M%S"
    desc = description.replace(",", "\\,").replace("\n", "\\n")
    summ = summary.replace(",", "\\,")
    return (
        f"BEGIN:VEVENT\n"
        f"UID:{uid}@larochebluegrass2026\n"
        f"DTSTART;TZID=Europe/Paris:{start_dt.strftime(fmt)}\n"
        f"DTEND;TZID=Europe/Paris:{end_dt.strftime(fmt)}\n"
        f"SUMMARY:{summ}\n"
        f"DESCRIPTION:{desc}\n"
        f"LOCATION:{location}\n"
        f"END:VEVENT"
    )

events  = []
counter = 1

# Main Stage
for row in data["main_stage"]:
    summary = f"🎸 {row['name']} — Main Stage | {FESTIVAL_NAME}"
    events.append(make_ics_event(
        f"blr2026-{counter:03d}", summary,
        DATE_MAP[row["date"]], row["start"], row["end"],
        row["notes"], FESTIVAL_LOCATION
    ))
    counter += 1

# Day Stage
for row in data["day_stage"]:
    summary = f"🎸 {row['name']} — Day Stage | {FESTIVAL_NAME}"
    events.append(make_ics_event(
        f"blr2026-{counter:03d}", summary,
        DATE_MAP[row["date"]], row["start"], row["end"],
        row["notes"], FESTIVAL_LOCATION
    ))
    counter += 1

# Street Festival — skip rows with no times set yet
for row in data["street_festival"]:
    stage   = row.get("stage", "Street Festival")
    summary = f"🎸 {row['name']} — {stage} | {FESTIVAL_NAME}"
    start   = row["start"] if row["start"] else "19:00"
    end     = row["end"]   if row["end"]   else "23:00"
    events.append(make_ics_event(
        f"blr2026-{counter:03d}", summary,
        DATE_MAP[row["date"]], start, end,
        row["notes"], FESTIVAL_LOCATION
    ))
    counter += 1

# Teaching Camp
for row in data["teaching_camp"]:
    summary = f"🎓 {row['name']} — Teaching Camp | {FESTIVAL_NAME}"
    events.append(make_ics_event(
        f"blr2026-{counter:03d}", summary,
        DATE_MAP[row["date"]], row["start"], row["end"],
        row["notes"], CAMP_LOCATION
    ))
    counter += 1

ics_content = (
    "BEGIN:VCALENDAR\n"
    "VERSION:2.0\n"
    f"PRODID:-//{FESTIVAL_NAME}//EN\n"
    "CALSCALE:GREGORIAN\n"
    "METHOD:PUBLISH\n"
    f"X-WR-CALNAME:{FESTIVAL_NAME}\n"
    "X-WR-TIMEZONE:Europe/Paris\n"
    f"X-WR-CALDESC:Full festival schedule for {FESTIVAL_NAME}\\, La Roche-sur-Foron\\, France. 30 July - 2 August 2026.\n"
    + "\n".join(events)
    + "\nEND:VCALENDAR\n"
)

ics_path = Path(__file__).parent / "LaRoche2026.ics"
ics_path.write_text(ics_content, encoding="utf-8")
print(f"ICS written: {counter - 1} events")


# =============================================================================
# XLSX GENERATION
# =============================================================================

# Colour palette
DARK_GREEN   = "1A3C34"
MID_GREEN    = "2D6A4F"
LIGHT_GREEN  = "D8F3DC"
GOLD         = "B7950B"
GOLD_LIGHT   = "FFF9C4"
WHITE        = "FFFFFF"
GREY_ROW     = "F4F4F4"
DARK_RED     = "8B0000"
STREET_BLUE  = "1A3A5C"
STREET_LIGHT = "D6E4F0"
CAMP_PURPLE  = "4A235A"
CAMP_LIGHT   = "EAD5F5"


def thin_border():
    s = Side(style="thin", color="CCCCCC")
    return Border(left=s, right=s, top=s, bottom=s)


def make_sheet(wb, title, rows, tab_color, header_color, light_row_color, is_first=False):
    """
    Build a formatted worksheet from a list of row dicts.
    Each row dict must have: date, name, country, start, end, notes.
    Optionally: stage (used as Stage Note column).
    """
    ws = wb.active if is_first else wb.create_sheet(title)
    ws.title = title
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = tab_color

    headers    = ["Date", "Band / Act", "Country", "Stage Note", "Start Time", "End Time", "Notes"]
    col_widths = [14,      36,           22,         20,           13,           13,          45]

    # Title banner
    ws.merge_cells("A1:G1")
    c = ws["A1"]
    c.value     = f"{FESTIVAL_NAME} — {title}"
    c.font      = Font(name="Arial", bold=True, size=14, color="FFFFFF")
    c.fill      = PatternFill("solid", fgColor=DARK_GREEN)
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    # Subtitle
    ws.merge_cells("A2:G2")
    c           = ws["A2"]
    c.value     = "Source data: data/schedule.json in the GitHub repository"
    c.font      = Font(name="Arial", italic=True, size=9, color="666666")
    c.alignment = Alignment(horizontal="center")
    ws.row_dimensions[2].height = 16

    # Column headers
    for col, (h, w) in enumerate(zip(headers, col_widths), 1):
        cell           = ws.cell(row=3, column=col, value=h)
        cell.font      = Font(name="Arial", bold=True, size=10, color="FFFFFF")
        cell.fill      = PatternFill("solid", fgColor=header_color)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border    = thin_border()
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[3].height = 20

    # Example row
    example = ["e.g. Thu 30 Jul", "e.g. Kristy Cox Band", "AU/US", "Main Stage",
               "19:00", "20:00", "Times in 24hr format"]
    for col, val in enumerate(example, 1):
        cell           = ws.cell(row=4, column=col, value=val)
        cell.font      = Font(name="Arial", size=9, italic=True, color="AAAAAA")
        cell.fill      = PatternFill("solid", fgColor="F0F0F0")
        cell.border    = thin_border()
        cell.alignment = Alignment(
            vertical="center",
            horizontal="center" if col in (5, 6) else "left",
            wrap_text=True
        )
    ws.row_dimensions[4].height = 24

    # Data rows
    current_date = None
    for i, row in enumerate(rows, start=5):
        is_tbc = row["name"].startswith("TBC")
        if row["date"] != current_date:
            current_date = row["date"]
            bg = light_row_color
        else:
            bg = GREY_ROW if i % 2 == 0 else WHITE
        if is_tbc:
            bg = "FFF3CD"

        values = [
            row["date"],
            row["name"],
            row.get("country", row.get("location", "")),
            row.get("stage", title),
            row["start"],
            row["end"],
            row["notes"],
        ]
        for col, val in enumerate(values, 1):
            cell           = ws.cell(row=i, column=col, value=val)
            cell.fill      = PatternFill("solid", fgColor=bg)
            cell.border    = thin_border()
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            cell.font      = Font(name="Arial", size=9, italic=is_tbc,
                                  color="888888" if is_tbc else "000000")
            if col in (5, 6):
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = Font(name="Arial", size=9, color=GOLD,
                                 bold=not is_tbc, italic=is_tbc)
        ws.row_dimensions[i].height = 30

    ws.freeze_panes = "A5"
    return ws


wb = Workbook()
make_sheet(wb, "Main Stage",      data["main_stage"],      MID_GREEN,   MID_GREEN,   LIGHT_GREEN, is_first=True)
make_sheet(wb, "Day Stage",       data["day_stage"],       GOLD,        GOLD,        GOLD_LIGHT,  is_first=False)
make_sheet(wb, "Street Festival", data["street_festival"], STREET_BLUE, STREET_BLUE, STREET_LIGHT,is_first=False)

# Teaching camp rows need a "stage" key for the Stage Note column
camp_rows = []
for row in data["teaching_camp"]:
    r = dict(row)
    r["country"] = r.pop("location", "")
    r["stage"]   = "Teaching Camp"
    camp_rows.append(r)
make_sheet(wb, "Teaching Camp", camp_rows, CAMP_PURPLE, CAMP_PURPLE, CAMP_LIGHT, is_first=False)

xlsx_path = Path(__file__).parent / "LaRoche2026_Festival_Schedule.xlsx"
wb.save(xlsx_path)
print(f"XLSX written: {xlsx_path}")
