from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()

DARK_GREEN  = "1A3C34"
MID_GREEN   = "2D6A4F"
LIGHT_GREEN = "D8F3DC"
GOLD        = "B7950B"
GOLD_LIGHT  = "FFF9C4"
WHITE       = "FFFFFF"
GREY_ROW    = "F4F4F4"
DARK_RED    = "8B0000"
STREET_BLUE = "1A3A5C"
STREET_LIGHT= "D6E4F0"

def thin_border():
    s = Side(style='thin', color="CCCCCC")
    return Border(left=s, right=s, top=s, bottom=s)

def make_sheet(wb, title, rows, tab_color, header_color, light_row_color, is_first=False):
    ws = wb.active if is_first else wb.create_sheet(title)
    ws.title = title
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.tabColor = tab_color

    headers = ["Date", "Band / Act", "Country", "Stage Note", "Start Time", "End Time", "Notes"]
    col_widths = [14, 36, 22, 20, 13, 13, 45]

    ws.merge_cells("A1:G1")
    title_cell = ws["A1"]
    title_cell.value = f"Bluegrass in La Roche 2026 — {title}"
    title_cell.font = Font(name="Arial", bold=True, size=14, color="FFFFFF")
    title_cell.fill = PatternFill("solid", fgColor=DARK_GREEN)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:G2")
    sub = ws["A2"]
    sub.value = "Fill in Start Time and End Time after consulting the schedule image on the festival website"
    sub.font = Font(name="Arial", italic=True, size=9, color="666666")
    sub.alignment = Alignment(horizontal="center")
    ws.row_dimensions[2].height = 16

    for col, (h, w) in enumerate(zip(headers, col_widths), 1):
        cell = ws.cell(row=3, column=col, value=h)
        cell.font = Font(name="Arial", bold=True, size=10, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=header_color)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = thin_border()
        ws.column_dimensions[get_column_letter(col)].width = w
    ws.row_dimensions[3].height = 20

    # Example row
    example = ["e.g. Thu 30 Jul", "e.g. Kristy Cox Band", "AU/US", "Main Stage", "19:00", "20:00", "Times in 24hr format — e.g. 19:00 to 20:00"]
    for col, val in enumerate(example, 1):
        cell = ws.cell(row=4, column=col, value=val)
        cell.font = Font(name="Arial", size=9, italic=True, color="AAAAAA")
        cell.fill = PatternFill("solid", fgColor="F0F0F0")
        cell.border = thin_border()
        cell.alignment = Alignment(vertical="center", horizontal="center" if col in (5, 6) else "left", wrap_text=True)
    ws.row_dimensions[4].height = 24

    current_date = None
    for i, row in enumerate(rows, start=5):
        is_tbc = row[1].startswith("TBC")
        if row[0] != current_date:
            current_date = row[0]
            bg = light_row_color
        else:
            bg = GREY_ROW if i % 2 == 0 else WHITE

        if is_tbc:
            bg = "FFF3CD"  # amber tint for TBC rows

        for col, val in enumerate(row, 1):
            cell = ws.cell(row=i, column=col, value=val)
            cell.font = Font(name="Arial", size=9, italic=is_tbc, color="888888" if is_tbc else "000000")
            cell.fill = PatternFill("solid", fgColor=bg)
            cell.border = thin_border()
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if col in (5, 6):
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.font = Font(name="Arial", size=9, color=GOLD, bold=not is_tbc, italic=is_tbc)
        ws.row_dimensions[i].height = 30

    ws.freeze_panes = "A5"
    return ws

# ── MAIN STAGE ────────────────────────────────────────────────────────────────
# Times and order taken directly from official schedule image
main_rows = [
    ["Thu 30 Jul", "Workshop Students & Teachers", "Europe",        "Main Stage", "17:30", "20:00", "End of teaching camp — students take the stage"],
    ["Thu 30 Jul", "Piotr Bulas & Garage Folks",   "PL",            "Main Stage", "20:00", "21:30", "Traditional Bluegrass with humour; luthier-led band"],
    ["Thu 30 Jul", "Opening Ceremony",              "",              "Main Stage", "21:30", "22:00", ""],
    ["Thu 30 Jul", "Paul & The Alley Cats",         "NL/ES",         "Main Stage", "22:00", "23:30", "European pioneers; Paul Von Vlodrop on mandolin"],
    ["Thu 30 Jul", "Kristy Cox Band",               "AU/US",         "Main Stage", "23:30", "01:00", "Nashville-based; 5 studio albums; returning since 2014"],
    ["Fri 31 Jul", "Noah Hassler-Forest",           "NL/ES",         "Main Stage", "18:00", "19:00", "Rotterdam contest winners; jazz & world music-infused Bluegrass"],
    ["Fri 31 Jul", "No Man's Land",                 "SK/US/NL/DK/BE","Main Stage", "19:00", "20:00", "All-female European supergroup; La Roche debut as full band"],
    ["Fri 31 Jul", "The New Aliquot & David Benda", "CZ",            "Main Stage", "20:00", "21:30", "Ondra Kozák; 4-time La Roche contest winners; 10th anniversary"],
    ["Fri 31 Jul", "Sentimental Gentlemen",         "US",            "Main Stage", "21:30", "23:00", "East Nashville; Sierra Ferrell's touring band"],
    ["Fri 31 Jul", "Veranda",                       "CA",            "Main Stage", "23:00", "00:30", "Montreal; Bluegrass in English and French"],
    ["Sat 1 Aug",  "Yonder Boys",                   "DE/US/AU/CL",   "Main Stage", "18:00", "19:00", "Berlin-based; Americana/Bluegrass/folk; promoted from Day Stage"],
    ["Sat 1 Aug",  "Sweet Sally",                   "US",            "Main Stage", "19:00", "20:00", "Young California trio; Berklee scholars; CBA stable"],
    ["Sat 1 Aug",  "Country Gongbang",              "KO",            "Main Stage", "20:00", "21:30", "Korean Bluegrass; IBMA grant recipients; Grand Ole Opry veterans"],
    ["Sat 1 Aug",  "Shelby Means Band",             "US",            "Main Stage", "21:30", "23:00", "2x Grammy winner (ex-Molly Tuttle); solo album 2025"],
    ["Sat 1 Aug",  "Monogram",                      "CZ",            "Main Stage", "23:00", "00:30", "30-year-old band; La Roche contest winners 2008; first visit in 10 years"],
    ["Sun 2 Aug",  "William Jack",                  "AU",            "Main Stage", "18:00", "19:00", "Solo cello; classically trained; Chris Thile & Tony Rice influences"],
    ["Sun 2 Aug",  "Blue Lass",                     "GB",            "Main Stage", "19:00", "20:00", "Promoted from Day Stage 2024; Bluegrass/Old Time/Folk mix"],
    ["Sun 2 Aug",  "Gadan",                         "IT/IE/US",      "Main Stage", "20:00", "21:15", "Celtic-Americana fusion; 3 banjo players incl. Enda Scahill (We Banjo Three)"],
    ["Sun 2 Aug",  "Hayde Bluegrass Orchestra",     "NO",            "Main Stage", "21:15", "22:30", "2x IBMA Momentum nominees 2022; touring US regulars"],
    ["Sun 2 Aug",  "Yellofox",                      "NL",            "Main Stage", "22:30", "00:00", "Folk-Americana; Paul Simon/Gram Parsons influences; festival closer"],
]

# ── DAY STAGE ─────────────────────────────────────────────────────────────────
day_rows = [
    ["Sat 1 Aug", "Kids on Bluegrass Europe",        "Europe",  "Day Stage", "12:00", "13:00", "Ages 6-16; two mornings of workshops culminating in performance"],
    ["Sat 1 Aug", "Kristy Cox Band",                 "AU/US",   "Day Stage", "13:00", "14:00", "Also headlining Thu Main Stage; second chance to see them"],
    ["Sat 1 Aug", "That's All Folk",                 "FR",      "Day Stage", "14:00", "15:00", "Local Alps trio; traditional Bluegrass + modern pop covers"],
    ["Sat 1 Aug", "The Sentimental Gentlemen",       "US",      "Day Stage", "15:00", "16:00", "Also on Main Stage Fri; Sierra Ferrell's touring band"],
    ["Sat 1 Aug", "Tim O'Connor Trio",               "IE/FR",   "Day Stage", "16:00", "17:00", "Irishman in Aix-les-Bains; folk/Irish/blues/rock trio"],
    ["Sun 2 Aug", "Grace Honeywell & Jeri Foreman",  "US/AU",   "Day Stage", "12:00", "13:00", "Twin fiddles; folk/country; formed in UK"],
    ["Sun 2 Aug", "Catch the Goat",                  "FR",      "Day Stage", "13:00", "14:00", "Toulouse veterans; Dawgrass style; mandocello & cello"],
    ["Sun 2 Aug", "Shelby Means Band",               "US",      "Day Stage", "14:00", "15:00", "Also on Sat Main Stage; entirely different set"],
    ["Sun 2 Aug", "Country Gongbang",                "KO",      "Day Stage", "15:00", "16:00", "Also on Sat Main Stage; final chance before they fly home"],
    ["Sun 2 Aug", "Sweet Sally",                     "US",      "Day Stage", "16:00", "17:00", "Also on Sat Main Stage; California trio"],
]

# ── STREET FESTIVAL ───────────────────────────────────────────────────────────
# 12 concerts on bar/restaurant/café terraces + 3 offsite in health centres
# Wed 29 Jul evening + Fri 31 Jul lunchtime. All free.
street_rows = [
    ["Wed 29 Jul", "TBC — Street Act 1", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Wed 29 Jul", "TBC — Street Act 2", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Wed 29 Jul", "TBC — Street Act 3", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Wed 29 Jul", "TBC — Street Act 4", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Wed 29 Jul", "TBC — Street Act 5", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Wed 29 Jul", "TBC — Street Act 6", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Wed 29 Jul", "TBC — Offsite Concert 1", "TBC", "Street Festival (Offsite)", "", "", "Health centre concert. FREE. Venue & band TBC — check festival website."],
    ["Fri 31 Jul", "TBC — Street Act 7", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Fri 31 Jul", "TBC — Street Act 8", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Fri 31 Jul", "TBC — Street Act 9", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Fri 31 Jul", "TBC — Street Act 10", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Fri 31 Jul", "TBC — Street Act 11", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Fri 31 Jul", "TBC — Street Act 12", "TBC", "Street Festival", "", "", "Bar/restaurant/café terraces around town centre. FREE. Band TBC — check festival website."],
    ["Fri 31 Jul", "TBC — Offsite Concert 2", "TBC", "Street Festival (Offsite)", "", "", "Health centre concert. FREE. Venue & band TBC — check festival website."],
    ["Fri 31 Jul", "TBC — Offsite Concert 3", "TBC", "Street Festival (Offsite)", "", "", "Health centre concert. FREE. Venue & band TBC — check festival website."],
]

make_sheet(wb, "Main Stage",     main_rows,   MID_GREEN,   MID_GREEN,   LIGHT_GREEN, is_first=True)
make_sheet(wb, "Day Stage",      day_rows,    GOLD,        GOLD,        GOLD_LIGHT,  is_first=False)
make_sheet(wb, "Street Festival",street_rows, STREET_BLUE, STREET_BLUE, STREET_LIGHT,is_first=False)

# ── TEACHING CAMP ─────────────────────────────────────────────────────────────
CAMP_PURPLE = "4A235A"
CAMP_LIGHT  = "EAD5F5"
camp_rows = [
    ["Mon 27 Jul", "Accommodation check-in",              "Lycée Sainte Famille", "14:00", "17:30", "School open for registration and room check-in"],
    ["Mon 27 Jul", "Welcome talk & drinks",               "Lycée Sainte Famille", "17:30", "20:00", "Welcome by Festival Chair and Camp Leader Gilles Rézard"],
    ["Mon 27 Jul", "Dinner",                              "Lycée Sainte Famille", "20:00", "21:30", ""],
    ["Tue 28 Jul", "Breakfast",                           "Lycée Sainte Famille", "07:45", "09:00", ""],
    ["Tue 28 Jul", "Today's news + Instrumental classes", "Lycée Sainte Famille", "09:00", "10:30", "Morning session 1 — instrumental classes"],
    ["Tue 28 Jul", "Break",                               "Lycée Sainte Famille", "10:30", "11:00", ""],
    ["Tue 28 Jul", "Instrumental classes",                "Lycée Sainte Famille", "11:00", "12:30", "Morning session 2 — instrumental classes"],
    ["Tue 28 Jul", "Lunch",                               "Lycée Sainte Famille", "12:30", "14:00", ""],
    ["Tue 28 Jul", "Wernick Method Jam: Instructions",    "Lycée Sainte Famille", "14:00", "16:00", "Afternoon — Wernick Method jam instructions"],
    ["Tue 28 Jul", "Break",                               "Lycée Sainte Famille", "16:00", "16:30", ""],
    ["Tue 28 Jul", "Optional/requested modules",                "Lycée Sainte Famille", "16:30", "19:00", "Requested/optional modules"],
    ["Tue 28 Jul", "Dinner",                              "Lycée Sainte Famille", "19:00", "20:30", ""],
    ["Wed 29 Jul", "Breakfast",                           "Lycée Sainte Famille", "07:45", "09:00", ""],
    ["Wed 29 Jul", "Today's news + Instrumental classes", "Lycée Sainte Famille", "09:00", "10:30", "Morning session 1 — instrumental classes"],
    ["Wed 29 Jul", "Break",                               "Lycée Sainte Famille", "10:30", "11:00", ""],
    ["Wed 29 Jul", "Instrumental classes",                "Lycée Sainte Famille", "11:00", "12:30", "Morning session 2 — instrumental classes"],
    ["Wed 29 Jul", "Lunch",                               "Lycée Sainte Famille", "12:30", "14:00", ""],
    ["Wed 29 Jul", "Wernick Method Jam: Coached jam",     "Lycée Sainte Famille", "14:00", "16:00", "Afternoon — coached Wernick Method jam"],
    ["Wed 29 Jul", "Break",                               "Lycée Sainte Famille", "16:00", "16:30", ""],
    ["Wed 29 Jul", "Concert rehearsal & organisation",             "Lycée Sainte Famille", "16:30", "18:00", "Rehearsal for Thursday student concert"],
    ["Wed 29 Jul", "Dinner",                              "Lycée Sainte Famille", "18:00", "19:00", ""],
    ["Thu 30 Jul", "Breakfast",                           "Lycée Sainte Famille", "07:45", "09:00", ""],
    ["Thu 30 Jul", "Today's news + Instrumental classes", "Lycée Sainte Famille", "09:00", "10:30", "Morning session 1 — instrumental classes"],
    ["Thu 30 Jul", "Break",                               "Lycée Sainte Famille", "10:30", "11:00", ""],
    ["Thu 30 Jul", "Band labs / jams",                    "Lycée Sainte Famille", "11:00", "12:30", "Final morning session — band labs and jams"],
    ["Thu 30 Jul", "Lunch",                               "Lycée Sainte Famille", "12:30", "14:00", ""],
    ["Thu 30 Jul", "Free time",                           "Lycée Sainte Famille", "14:00", "16:00", ""],
    ["Thu 30 Jul", "Break",                               "Lycée Sainte Famille", "16:00", "16:30", ""],
    ["Thu 30 Jul", "Head to festival site",               "Lycée Sainte Famille", "16:30", "17:30", "Move to Lycée Sainte Marie festival site"],
    ["Thu 30 Jul", "Students concert — Main Stage",       "Festival Main Stage",  "17:30", "19:00", "Band Labs perform on the Main Stage"],
    ["Thu 30 Jul", "French teachers set — Main Stage",    "Festival Main Stage",  "19:00", "20:00", "French teachers perform on the Main Stage"],
]
make_sheet(wb, "Teaching Camp", camp_rows, CAMP_PURPLE, CAMP_PURPLE, CAMP_LIGHT, is_first=False)

# ── GOOGLE CALENDAR IMPORT ────────────────────────────────────────────────────
gc = wb.create_sheet("Google Calendar Import")
gc.sheet_properties.tabColor = DARK_RED
gc.sheet_view.showGridLines = False

gc.merge_cells("A1:F1")
t = gc["A1"]
t.value = "Google Calendar Import — fill in times, then export this sheet as CSV and import into Google Calendar"
t.font = Font(name="Arial", bold=True, size=11, color="FFFFFF")
t.fill = PatternFill("solid", fgColor=DARK_RED)
t.alignment = Alignment(horizontal="center", vertical="center")
gc.row_dimensions[1].height = 26

gc.merge_cells("A2:F2")
note = gc["A2"]
note.value = "TBC rows are placeholders for the Street Festival — update when the festival publishes the full street programme"
note.font = Font(name="Arial", italic=True, size=9, color="888888")
note.alignment = Alignment(horizontal="center")
gc.row_dimensions[2].height = 16

gc_headers = ["Subject", "Start Date", "Start Time", "End Date", "End Time", "Description"]
gc_widths   = [50, 14, 13, 14, 13, 60]
for col, (h, w) in enumerate(zip(gc_headers, gc_widths), 1):
    cell = gc.cell(row=3, column=col, value=h)
    cell.font = Font(name="Arial", bold=True, size=10, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=DARK_RED)
    cell.alignment = Alignment(horizontal="center")
    cell.border = thin_border()
    gc.column_dimensions[get_column_letter(col)].width = w

date_map = {
    "Mon 27 Jul": "27/07/2026",
    "Tue 28 Jul": "28/07/2026",
    "Wed 29 Jul": "29/07/2026",
    "Thu 30 Jul": "30/07/2026",
    "Fri 31 Jul": "31/07/2026",
    "Sat 1 Aug":  "01/08/2026",
    "Sun 2 Aug":  "02/08/2026",
}

all_rows = (
    [(r, "Main Stage")      for r in main_rows] +
    [(r, "Day Stage")       for r in day_rows] +
    [(r, "Street Festival") for r in street_rows] +
    [(r, "Teaching Camp")   for r in camp_rows]
)

for i, (row, stage) in enumerate(all_rows, start=4):
    date_str = date_map.get(row[0], row[0])
    is_tbc = row[1].startswith("TBC")
    subject = f"{row[1]} ({row[2]}) — {stage}"
    desc = row[6] if len(row) > 6 else ""
    vals = [subject, date_str, row[4], date_str, row[5], desc]
    bg = "FFF3CD" if is_tbc else (GREY_ROW if i % 2 == 0 else WHITE)
    for col, val in enumerate(vals, 1):
        cell = gc.cell(row=i, column=col, value=val)
        cell.font = Font(name="Arial", size=9, italic=is_tbc, color="888888" if is_tbc else "000000")
        cell.fill = PatternFill("solid", fgColor=bg)
        cell.border = thin_border()
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    gc.row_dimensions[i].height = 20

gc.freeze_panes = "A3"

wb.save("/home/claude/LaRoche2026_Festival_Schedule.xlsx")
print("Done")
