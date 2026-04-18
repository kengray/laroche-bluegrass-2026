# =============================================================================
# generate_ics.py
# Generates a .ics calendar file for the Bluegrass in La Roche 2026 festival.
#
# Requires: no external libraries — uses only Python's built-in datetime module
# Output:   LaRoche2026.ics
#
# The .ics format (iCalendar) is the standard for calendar data exchange.
# The file can be:
#   - Imported directly into Google Calendar, Apple Calendar, Outlook etc.
#   - Hosted on a public URL (e.g. GitHub raw) and subscribed to, so that
#     any updates to the file are automatically reflected in subscribers'
#     calendars (Google Calendar re-fetches subscribed URLs roughly daily).
#
# Events are grouped into four categories:
#   🎸 Main Stage     — evening concerts
#   🎸 Day Stage      — lunchtime concerts
#   🎸 Street Festival — free outdoor concerts (TBC placeholders)
#   🎓 Teaching Camp  — residential camp sessions (different location)
# =============================================================================

from datetime import datetime, timedelta


def make_event(uid, summary, date_str, start_time, end_time, description,
               location="La Roche-sur-Foron, France"):
    """
    Builds a single VEVENT block as a string, ready to be included in a
    VCALENDAR document.

    Parameters
    ----------
    uid         : str  — unique identifier for this event (e.g. "blr2026-001")
    summary     : str  — event title shown in the calendar
    date_str    : str  — date in DD/MM/YYYY format (e.g. "30/07/2026")
    start_time  : str  — start time in HH:MM 24hr format (e.g. "20:00")
    end_time    : str  — end time in HH:MM 24hr format (e.g. "21:30")
                         If end_time <= start_time, it is assumed to be past
                         midnight and one day is added automatically
    description : str  — optional notes shown in the event detail view
    location    : str  — venue/address string

    Returns
    -------
    str : a complete BEGIN:VEVENT ... END:VEVENT block
    """

    # Parse the date string into a datetime object
    date = datetime.strptime(date_str, "%d/%m/%Y")

    # Extract hours and minutes from the HH:MM time strings
    sh, sm = int(start_time[:2]), int(start_time[3:])
    eh, em = int(end_time[:2]),   int(end_time[3:])

    # Combine date and time into full datetime objects
    start_dt = date.replace(hour=sh, minute=sm)
    end_dt   = date.replace(hour=eh, minute=em)

    # Handle acts that finish after midnight (e.g. 23:30 start, 01:00 end)
    # If end is earlier than or equal to start, the act crosses midnight
    if end_dt <= start_dt:
        end_dt += timedelta(days=1)

    # iCalendar datetime format: YYYYMMDDTHHmmSS
    fmt = "%Y%m%dT%H%M%S"

    # Escape commas and newlines in text fields as required by the iCal spec
    desc = description.replace(",", "\\,").replace("\n", "\\n")
    summ = summary.replace(",", "\\,")

    # Build the VEVENT block. TZID=Europe/Paris ensures times display correctly
    # regardless of the subscriber's local timezone.
    return f"""BEGIN:VEVENT
UID:{uid}@larochebluegrass2026
DTSTART;TZID=Europe/Paris:{start_dt.strftime(fmt)}
DTEND;TZID=Europe/Paris:{end_dt.strftime(fmt)}
SUMMARY:{summ}
DESCRIPTION:{desc}
LOCATION:{location}
END:VEVENT"""


# =============================================================================
# DATE LOOKUP TABLE
# Maps the human-readable date strings used in the data rows to the
# DD/MM/YYYY format that make_event() expects.
# =============================================================================
date_map = {
    "Mon 27 Jul": "27/07/2026",
    "Tue 28 Jul": "28/07/2026",
    "Wed 29 Jul": "29/07/2026",
    "Thu 30 Jul": "30/07/2026",
    "Fri 31 Jul": "31/07/2026",
    "Sat 1 Aug":  "01/08/2026",
    "Sun 2 Aug":  "02/08/2026",
}


# =============================================================================
# SCHEDULE DATA
# Each row is a list: [date, name, stage, start_time, end_time, description]
# Times are 24hr. End times past midnight are handled automatically.
# Source: official schedule image from larochebluegrass.org
# =============================================================================

# -----------------------------------------------------------------------------
# MAIN STAGE — evening concerts
# Each act ends when the next one starts on the same night.
# Closing acts each night have estimated end times (~90 mins).
# -----------------------------------------------------------------------------
main_rows = [
    # Thursday 30 July — festival opening night
    ["Thu 30 Jul", "Workshop Students & Teachers",  "Main Stage", "17:30", "20:00", "End of teaching camp — students take the stage"],
    ["Thu 30 Jul", "Piotr Bulas & Garage Folks",    "Main Stage", "20:00", "21:30", "Traditional Bluegrass with humour; luthier-led band (PL)"],
    ["Thu 30 Jul", "Opening Ceremony",               "Main Stage", "21:30", "22:00", ""],
    ["Thu 30 Jul", "Paul & The Alley Cats",          "Main Stage", "22:00", "23:30", "European pioneers; Paul Von Vlodrop on mandolin (NL/ES)"],
    ["Thu 30 Jul", "Kristy Cox Band",                "Main Stage", "23:30", "01:00", "Nashville-based; 5 studio albums; returning since 2014 (AU/US)"],
    # Friday 31 July
    ["Fri 31 Jul", "Noah Hassler-Forest",            "Main Stage", "18:00", "19:00", "Rotterdam contest winners; jazz & world music-infused Bluegrass (NL/ES)"],
    ["Fri 31 Jul", "No Man's Land",                  "Main Stage", "19:00", "20:00", "All-female European supergroup; La Roche debut as full band (SK/US/NL/DK/BE)"],
    ["Fri 31 Jul", "The New Aliquot & David Benda",  "Main Stage", "20:00", "21:30", "Ondra Kozák; 4-time La Roche contest winners; 10th anniversary (CZ)"],
    ["Fri 31 Jul", "Sentimental Gentlemen",          "Main Stage", "21:30", "23:00", "East Nashville; Sierra Ferrell's touring band (US)"],
    ["Fri 31 Jul", "Veranda",                        "Main Stage", "23:00", "00:30", "Montreal; Bluegrass in English and French (CA)"],
    # Saturday 1 August
    ["Sat 1 Aug",  "Yonder Boys",                    "Main Stage", "18:00", "19:00", "Berlin-based; Americana/Bluegrass/folk (DE/US/AU/CL)"],
    ["Sat 1 Aug",  "Sweet Sally",                    "Main Stage", "19:00", "20:00", "Young California trio; Berklee scholars (US)"],
    ["Sat 1 Aug",  "Country Gongbang",               "Main Stage", "20:00", "21:30", "Korean Bluegrass; IBMA grant recipients; Grand Ole Opry veterans (KO)"],
    ["Sat 1 Aug",  "Shelby Means Band",              "Main Stage", "21:30", "23:00", "2x Grammy winner (ex-Molly Tuttle); solo album 2025 (US)"],
    ["Sat 1 Aug",  "Monogram",                       "Main Stage", "23:00", "00:30", "30-year-old band; La Roche contest winners 2008 (CZ)"],
    # Sunday 2 August — final night
    ["Sun 2 Aug",  "William Jack",                   "Main Stage", "18:00", "19:00", "Solo cello; classically trained; Chris Thile & Tony Rice influences (AU)"],
    ["Sun 2 Aug",  "Blue Lass",                      "Main Stage", "19:00", "20:00", "Promoted from Day Stage 2024; Bluegrass/Old Time/Folk mix (GB)"],
    ["Sun 2 Aug",  "Gadan",                          "Main Stage", "20:00", "21:15", "Celtic-Americana fusion; 3 banjo players incl. Enda Scahill (IT/IE/US)"],
    ["Sun 2 Aug",  "Hayde Bluegrass Orchestra",      "Main Stage", "21:15", "22:30", "2x IBMA Momentum nominees 2022 (NO)"],
    ["Sun 2 Aug",  "Yellofox",                       "Main Stage", "22:30", "00:00", "Folk-Americana; festival closer (NL)"],
]

# -----------------------------------------------------------------------------
# DAY STAGE — lunchtime concerts, Saturday & Sunday, 12:00-17:00
# Each slot is exactly 1 hour per the official schedule image.
# -----------------------------------------------------------------------------
day_rows = [
    # Saturday 1 August
    ["Sat 1 Aug", "Kids on Bluegrass Europe",       "Day Stage", "12:00", "13:00", "Ages 6-16 workshop performance"],
    ["Sat 1 Aug", "Kristy Cox Band",                "Day Stage", "13:00", "14:00", "Also headlining Thu Main Stage (AU/US)"],
    ["Sat 1 Aug", "That's All Folk",                "Day Stage", "14:00", "15:00", "Local Alps trio; traditional Bluegrass + pop covers (FR)"],
    ["Sat 1 Aug", "The Sentimental Gentlemen",      "Day Stage", "15:00", "16:00", "Also on Main Stage Fri; Sierra Ferrell's touring band (US)"],
    ["Sat 1 Aug", "Tim O'Connor Trio",              "Day Stage", "16:00", "17:00", "Irishman in Aix-les-Bains; folk/Irish/blues/rock (IE/FR)"],
    # Sunday 2 August
    ["Sun 2 Aug", "Grace Honeywell & Jeri Foreman", "Day Stage", "12:00", "13:00", "Twin fiddles; folk/country (US/AU)"],
    ["Sun 2 Aug", "Catch the Goat",                 "Day Stage", "13:00", "14:00", "Toulouse veterans; Dawgrass style (FR)"],
    ["Sun 2 Aug", "Shelby Means Band",              "Day Stage", "14:00", "15:00", "Also on Sat Main Stage; different set (US)"],
    ["Sun 2 Aug", "Country Gongbang",               "Day Stage", "15:00", "16:00", "Also on Sat Main Stage (KO)"],
    ["Sun 2 Aug", "Sweet Sally",                    "Day Stage", "16:00", "17:00", "Also on Sat Main Stage; California trio (US)"],
]

# -----------------------------------------------------------------------------
# STREET FESTIVAL — free concerts on café/bar terraces around town
# Wednesday evening and Friday lunchtime.
# Placeholder events only — full programme not yet published.
# Replace these rows when the festival publishes the street line-up.
# -----------------------------------------------------------------------------
street_rows = [
    ["Wed 29 Jul", "TBC — Street Festival",          "Street Festival", "19:00", "23:00", "Live music on bar/restaurant/café terraces around town centre. FREE. Full programme TBC."],
    ["Fri 31 Jul", "TBC — Street Festival Lunchtime","Street Festival", "12:00", "14:00", "Live music on bar/restaurant/café terraces around town centre. FREE. Full programme TBC."],
]

# -----------------------------------------------------------------------------
# TEACHING CAMP — residential bluegrass camp, Mon 27 – Thu 30 July
# Held at Lycée Sainte Famille, La Roche-sur-Foron.
# Uses a separate location string and 🎓 emoji to distinguish from concerts.
# Timetable source: official timetable image on larochebluegrass.org/adult-teaching-camp
# -----------------------------------------------------------------------------
camp_rows = [
    # Monday 27 July — arrival day
    ["Mon 27 Jul", "Accommodation check-in",               "Teaching Camp", "14:00", "17:30", "School open for registration and room check-in"],
    ["Mon 27 Jul", "Welcome talk & drinks",                 "Teaching Camp", "17:30", "20:00", "Welcome by Festival Chair and Camp Leader Gilles Rézard"],
    ["Mon 27 Jul", "Dinner",                                "Teaching Camp", "20:00", "21:30", "Welcome dinner"],
    # Tuesday 28 July — first full teaching day
    ["Tue 28 Jul", "Breakfast",                             "Teaching Camp", "07:45", "09:00", ""],
    ["Tue 28 Jul", "Today's news + Instrumental classes",   "Teaching Camp", "09:00", "10:30", "Morning session 1 — instrumental classes on chosen instrument"],
    ["Tue 28 Jul", "Break",                                 "Teaching Camp", "10:30", "11:00", ""],
    ["Tue 28 Jul", "Instrumental classes",                  "Teaching Camp", "11:00", "12:30", "Morning session 2 — instrumental classes"],
    ["Tue 28 Jul", "Lunch",                                 "Teaching Camp", "12:30", "14:00", ""],
    ["Tue 28 Jul", "Wernick Method Jam: Instructions",      "Teaching Camp", "14:00", "16:00", "Introduction to the Wernick Method coached jam format"],
    ["Tue 28 Jul", "Break",                                 "Teaching Camp", "16:00", "16:30", ""],
    ["Tue 28 Jul", "Optional/requested modules",            "Teaching Camp", "16:30", "19:00", "Participant-requested workshop modules"],
    ["Tue 28 Jul", "Dinner",                                "Teaching Camp", "19:00", "20:30", ""],
    # Wednesday 29 July — second full teaching day
    ["Wed 29 Jul", "Breakfast",                             "Teaching Camp", "07:45", "09:00", ""],
    ["Wed 29 Jul", "Today's news + Instrumental classes",   "Teaching Camp", "09:00", "10:30", "Morning session 1 — instrumental classes"],
    ["Wed 29 Jul", "Break",                                 "Teaching Camp", "10:30", "11:00", ""],
    ["Wed 29 Jul", "Instrumental classes",                  "Teaching Camp", "11:00", "12:30", "Morning session 2 — instrumental classes"],
    ["Wed 29 Jul", "Lunch",                                 "Teaching Camp", "12:30", "14:00", ""],
    ["Wed 29 Jul", "Wernick Method Jam: Coached jam",       "Teaching Camp", "14:00", "16:00", "Coached jam session using the Wernick Method"],
    ["Wed 29 Jul", "Break",                                 "Teaching Camp", "16:00", "16:30", ""],
    ["Wed 29 Jul", "Concert rehearsal & organisation",      "Teaching Camp", "16:30", "18:00", "Preparation and rehearsal for the Thursday student concert"],
    ["Wed 29 Jul", "Dinner",                                "Teaching Camp", "18:00", "19:00", ""],
    # Thursday 30 July — final camp day; students perform at the festival
    ["Thu 30 Jul", "Breakfast",                             "Teaching Camp", "07:45", "09:00", ""],
    ["Thu 30 Jul", "Today's news + Instrumental classes",   "Teaching Camp", "09:00", "10:30", "Morning session 1 — instrumental classes"],
    ["Thu 30 Jul", "Break",                                 "Teaching Camp", "10:30", "11:00", ""],
    ["Thu 30 Jul", "Band labs / jams",                      "Teaching Camp", "11:00", "12:30", "Final session — band labs and jams before the student concert"],
    ["Thu 30 Jul", "Lunch",                                 "Teaching Camp", "12:30", "14:00", ""],
    ["Thu 30 Jul", "Free time",                             "Teaching Camp", "14:00", "16:00", ""],
    ["Thu 30 Jul", "Break",                                 "Teaching Camp", "16:00", "16:30", ""],
    ["Thu 30 Jul", "Head to festival site",                 "Teaching Camp", "16:30", "17:30", "Travel to Lycée Sainte Marie festival site"],
    ["Thu 30 Jul", "Students concert — Main Stage",         "Teaching Camp", "17:30", "19:00", "Band Labs groups perform on the Main Stage — festival opens"],
    ["Thu 30 Jul", "French teachers set — Main Stage",      "Teaching Camp", "19:00", "20:00", "French teaching staff perform on the Main Stage"],
]


# =============================================================================
# BUILD THE EVENT LIST
# Iterate over all four data sets, look up the full date, build the summary
# string, set the correct location, and call make_event() for each row.
# =============================================================================
events      = []
uid_counter = 1   # Sequential counter used to give each event a unique UID

for row in main_rows + day_rows + street_rows + camp_rows:
    date_key = row[0]                          # e.g. "Thu 30 Jul"
    name     = row[1]                          # Act/session name
    stage    = row[2]                          # Stage or category label
    start    = row[3]                          # Start time HH:MM
    end      = row[4]                          # End time HH:MM
    desc     = row[5]                          # Description / notes

    # Teaching Camp events use a different physical location
    loc = ("Lycée Sainte Famille, La Roche-sur-Foron, France"
           if stage == "Teaching Camp"
           else "La Roche-sur-Foron, France")

    # Different emoji prefix to visually distinguish camp from concert events
    emoji   = "🎓" if stage == "Teaching Camp" else "🎸"
    summary = f"{emoji} {name} — {stage} | Bluegrass La Roche 2026"

    # Format the UID with zero-padded counter for clean sorting
    uid = f"blr2026-{uid_counter:03d}"

    events.append(make_event(uid, summary, date_map[date_key], start, end, desc,
                             location=loc))
    uid_counter += 1


# =============================================================================
# ASSEMBLE AND WRITE THE .ICS FILE
# The VCALENDAR wrapper is required by the iCalendar spec.
# X-WR-* properties are Apple/Google extensions that set the calendar name
# and description shown when a user subscribes.
# =============================================================================
ics = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Bluegrass in La Roche 2026//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:Bluegrass in La Roche 2026
X-WR-TIMEZONE:Europe/Paris
X-WR-CALDESC:Full festival schedule for Bluegrass in La Roche 2026\\, La Roche-sur-Foron\\, France. 30 July - 2 August 2026.
""" + "\n".join(events) + "\nEND:VCALENDAR\n"

# Write the file as UTF-8 to preserve emoji and accented characters
with open("/home/claude/LaRoche2026.ics", "w", encoding="utf-8") as f:
    f.write(ics)

print(f"Done — {uid_counter - 1} events written")
