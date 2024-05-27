import p2app.events

def search(event, cursor):
    """Initiates a search for regions and return a RegionSearchResultEvent list"""
    try:
        event_list = []

        query = "SELECT * FROM region WHERE "
        params = []
        conditions = []

        if event.region_code() is not None:
            conditions.append('region_code = ?')
            params.append(event.region_code())
        if event.local_code() is not None:
            conditions.append('local_code = ?')
            params.append(event.local_code())
        if event.name() is not None:
            conditions.append('name = ?')
            params.append(event.name())

        if conditions:
            query += ' AND '.join(conditions)

        cursor.execute(query, params)

        rows = cursor.fetchall()

        for row in rows:
            event_list.append(
                p2app.events.regions.RegionSearchResultEvent(p2app.events.regions.Region
                                                             (row[0], row[1], row[2], row[3],
                                                              row[4], row[5], row[6], row[7])))
        return event_list
    except Exception:
        pass

def load(event, cursor):
    """loads a region from the database to edit it"""
    cursor.execute("SELECT * FROM region WHERE region_id = ?",
                        (event.region_id(),))

    row = cursor.fetchone()

    return p2app.events.regions.RegionLoadedEvent(p2app.events.regions.Region
                                                 (row[0], row[1], row[2], row[3],
                                                  row[4], row[5], row[6], row[7]))

def update(event, cursor, conn):
    """saves a new region into the database"""
    try:
        cursor.execute("UPDATE region SET region_code = ?, "
                            "local_code = ?, name = ?, continent_id = ?, country_id = ?,"
                            " wikipedia_link = ?, keywords = ? WHERE region_id = ?",
                            (event.region().region_code,
                             event.region().local_code, event.region().name,
                             event.region().continent_id, event.region().country_id,
                             event.region().wikipedia_link, event.region().keywords,
                             event.region().region_id))
        conn.commit()

        return p2app.events.regions.RegionSavedEvent(p2app.events.regions.Region
                                                    (event.region().region_id,
                                                     event.region().region_code,
                                                     event.region().local_code, event.region().name,
                                                     event.region().continent_id,
                                                     event.region().country_id,
                                                     event.region().wikipedia_link,
                                                     event.region().keywords))


    except Exception as e:
        return p2app.events.regions.SaveRegionFailedEvent(e)

def add_new(event, cursor, conn):
    """saves a modified region into the database"""
    try:
        cursor.execute("INSERT INTO region (region_id, region_code, local_code, name,"
                            " continent_id, country_id, wikipedia_link, keywords) VALUES "
                            "(?, ?, ?, ?, ?, ?, ?, ?)", (event.region().region_id,
                                                         event.region().region_code,
                                                         event.region().local_code,
                                                         event.region().name,
                                                         event.region().continent_id,
                                                         event.region().country_id,
                                                         event.region().wikipedia_link,
                                                         event.region().keywords))

        conn.commit()

        cursor.execute("SELECT * from region WHERE region_code = ?",
                            (event.region().region_code,))

        row = cursor.fetchone()

        return p2app.events.regions.RegionSavedEvent(
            p2app.events.regions.Region(row[0], row[1], row[2],
                                        row[3], row[4], row[5], row[6], row[7]))

    except Exception as e:
        return p2app.events.regions.SaveRegionFailedEvent(e)
