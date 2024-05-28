import p2app.events

def search(event, cursor):
    """Initiates a search for countries and return a StartCountrySearchEvent list"""
    try:
        event_list = []
        if event.country_code() is not None and event.name() is None:
            cursor.execute("SELECT * FROM country WHERE country_code = ?",
                                (event.country_code(),))
            row = cursor.fetchone()
            event_list.append(p2app.events.countries.
            CountrySearchResultEvent(
                p2app.events.countries.Country(row[0], row[1], row[2], row[3], row[4], row[5])))

        elif event.country_code() is None and event.name() is not None:
            cursor.execute("SELECT * FROM country WHERE name = ?",
                                (event.name(),))
            rows = cursor.fetchall()
            for row in rows:
                event_list.append(p2app.events.countries.CountrySearchResultEvent(
                    p2app.events.countries.Country(row[0], row[1], row[2], row[3], row[4],
                                                   row[5])))

        else:
            cursor.execute("SELECT * FROM country WHERE country_code = ? AND "
                                "name = ?", (event.country_code(), event.name(),))
            row = cursor.fetchone()
            event_list.append(p2app.events.countries.
            CountrySearchResultEvent(
                p2app.events.countries.Country(row[0], row[1], row[2], row[3], row[4], row[5])))

        return event_list
    except Exception:
        pass

def load(event, cursor):
    """loads a country from the database to edit it"""
    cursor.execute("SELECT * FROM country WHERE country_id = ?",
                        (event.country_id(),))
    row = cursor.fetchone()
    return p2app.events.countries.CountryLoadedEvent(
        p2app.events.countries.Country(row[0], row[1], row[2], row[3], row[4], row[5]))
def update(event, cursor, conn):
    """saves a new country into the database"""
    try:
        cursor.execute(
            "UPDATE country SET country_code = ?, name = ?, continent_id = ?,"
            " wikipedia_link = ?, keywords = ? WHERE country_id = ?",
            (event.country().country_code, event.country().name,
             event.country().continent_id, event.country().wikipedia_link,
             event.country().keywords, event.country().country_id))

        conn.commit()

        return p2app.events.countries.CountrySavedEvent(p2app.events.countries.Country(
            event.country().country_id, event.country().country_code, event.country().name,
            event.country().continent_id, event.country().wikipedia_link,
            event.country().keywords))

    except Exception as e:
        return p2app.events.countries.SaveCountryFailedEvent(e)

def add_new(event, cursor, conn):
    """saves a modified country into the database"""
    try:
        cursor.execute("INSERT INTO country (country_id, country_code, name, "
                            "continent_id, wikipedia_link, keywords) VALUES (?,?,?,?,?,?)",
                            (event.country().country_id,
                             event.country().country_code, event.country().name,
                             event.country().continent_id, event.country().wikipedia_link,
                             event.country().keywords))

        conn.commit()

        row = cursor.execute("SELECT * FROM country WHERE country_code = ?"
                                  , (event.country().country_code,)).fetchone()

        return (p2app.events.countries.CountrySavedEvent
               (p2app.events.countries.Country(row[0], row[1], row[2], row[3], row[4], row[5])))

    except Exception as e:
        return p2app.events.countries.SaveCountryFailedEvent(e)

