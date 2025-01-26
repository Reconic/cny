#!/usr/bin/env python3
import datetime
import lunardate

def get_animal(year):
    """Get the presiding animal zodiac for a given year."""
    animals = [
        "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", 
        "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"
    ]
    return animals[(year - 1900) % len(animals)]

def cny_gregorian(year):
    """Get the date in the Gregorian calendar of CNY for a given year."""
    if year < 1900 or year > 2099:
        raise ValueError(
            f"Year {year} is outside the scope of lunardate (1900-2099)"
        )
    return lunardate.LunarDate(year, 1, 1).toSolarDate()

def gen_ical_vevent(year):
    """Generate iCalendar events for CNY reunion dinner and holiday period."""
    events = []
    
    # Reunion Dinner (1 day before CNY)
    reunion_date = cny_gregorian(year) - datetime.timedelta(days=1)
    reunion_event = "\r\n".join([
        "BEGIN:VEVENT",
        f"DTSTAMP:{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
        f"UID:{year}-reunion@github.com/reconic/cny.ics",
        f"DTSTART;VALUE=DATE:{reunion_date.strftime('%Y%m%d')}",
        f"DTEND;VALUE=DATE:{(reunion_date + datetime.timedelta(days=1)).strftime('%Y%m%d')}",
        "SUMMARY;LANGUAGE=en-GB:Chinese New Year Reunion Dinner",
        f"DESCRIPTION;LANGUAGE=en-GB:Reunion Dinner for the Year of the {get_animal(year)}",
        "END:VEVENT"
    ])
    events.append(reunion_event)
    
    # Extended CNY Holiday (14 days)
    cny_start = cny_gregorian(year)
    for day in range(14):
        holiday_date = cny_start + datetime.timedelta(days=day)
        holiday_event = "\r\n".join([
            "BEGIN:VEVENT",
            f"DTSTAMP:{datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"UID:{year}-cny-{day+1}@github.com/reconic/cny.ics",
            f"DTSTART;VALUE=DATE:{holiday_date.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{(holiday_date + datetime.timedelta(days=1)).strftime('%Y%m%d')}",
            "SUMMARY;LANGUAGE=en-GB:Chinese New Year Holiday",
            f"DESCRIPTION;LANGUAGE=en-GB:Day {day+1} of 14 - Year of the {get_animal(year)}",
            "END:VEVENT"
        ])
        events.append(holiday_event)
    
    return "\r\n".join(events)

def main():
    vcal_header = "\r\n".join([
        "BEGIN:VCALENDAR",
        "PRODID:-//reconic//cny.ics//EN",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
    ])
    
    vcal_body = "\r\n".join([gen_ical_vevent(year) for year in range(1900, 2100)])
    vcal_footer = "END:VCALENDAR"
    
    vcal = "\r\n".join([vcal_header, vcal_body, vcal_footer])
    print(vcal)

if __name__ == "__main__":
    main()
