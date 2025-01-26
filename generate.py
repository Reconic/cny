#!/usr/bin/env python3  

import datetime
import lunardate
import uuid

def get_animal(year):
    """Get the presiding animal zodiac for a given year."""
    animals = [
        "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", 
        "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig",
    ]
    return animals[(year - 1900) % len(animals)]

def cny_gregorian(year):
    """Get the date in the Gregorian calendar of CNY for a given year."""
    if year < 1900 or year > 2099:
        raise ValueError(f"Year {year} is outside the scope of lunardate (1900-2099)")
    return lunardate.LunarDate(year, 1, 1).toSolarDate()

def gen_ical_vevent(year, start_date, end_date, summary, description):
    """Generate an iCalendar VEVENT for a given date range as a text string."""
    uid = f"{year}-{start_date.strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}@cny.ics"
    return "\r\n".join(
        [
            "BEGIN:VEVENT",
            f"DTSTAMP:{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
            f"UID:{uid}",
            f"DTSTART;VALUE=DATE:{start_date.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{end_date.strftime('%Y%m%d')}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{description}",
            "END:VEVENT",
            ""
        ]
    )

def main():
    vcal_header = "\r\n".join(
        [
            "BEGIN:VCALENDAR",
            "PRODID:-//reconic//cny.ics//EN",
            "VERSION:2.0",
            "CALSCALE:GREGORIAN",
        ]
    )
    
    vcal_body = ""
    
    for year in range(1999, 2100):  # Range from 1999 to 2099
        cny_date = cny_gregorian(year)
        
        # Generate Reunion Dinner event (1 day before CNY)
        reunion_dinner_date = cny_date - datetime.timedelta(days=1)
        vcal_body += gen_ical_vevent(
            year, 
            reunion_dinner_date, 
            reunion_dinner_date + datetime.timedelta(days=1), 
            "Reunion Dinner", 
            f"Gathering for the Year of the {get_animal(year)}"
        )
        
        # Generate Chinese New Year event (CNY day)
        vcal_body += gen_ical_vevent(
            year, 
            cny_date, 
            cny_date + datetime.timedelta(days=1), 
            "Chinese New Year", 
            f"Year of the {get_animal(year)}"
        )
        
        # Generate Chinese New Year Holiday (2 weeks after CNY)
        two_week_end_date = cny_date + datetime.timedelta(days=14)
        vcal_body += gen_ical_vevent(
            year, 
            cny_date, 
            two_week_end_date, 
            "Chinese New Year Holiday", 
            f"Celebrating the Year of the {get_animal(year)}"
        )
    
    vcal_footer = "END:VCALENDAR"
    
    # Print the iCalendar content for manual saving
    print("\r\n".join([vcal_header, vcal_body, vcal_footer]))

if __name__ == "__main__":
    main()
