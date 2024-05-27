import p2app.events

def search(event, cursor):
    """Initiates a search for continents and return a ContinentSearchResultEvent list"""
    try:
        event_list = []
        if event.name() is None and event.continent_code() is not None:
            cursor.execute(
                "SELECT continent_id, name FROM continent WHERE continent_code"
                " = ?", (event.continent_code(),))
            id_ = cursor.fetchone()

            event_list.append((p2app.events.continents.ContinentSearchResultEvent
                   (p2app.events.continents.Continent(id_[0], event.continent_code()
                                                      , id_[1]))))

        elif event.name() is not None and event.continent_code() is None:
            cursor.execute(
                "SELECT continent_id, continent_code FROM continent WHERE name"
                " = ?", (event.name(),))
            id_ = cursor.fetchall()
            for row in id_:
                event_list.append((p2app.events.continents.ContinentSearchResultEvent
                       (p2app.events.continents.Continent(row[0], row[1], event.name()))))

        else:
            cursor.execute(
                "SELECT continent_id FROM continent WHERE name"
                " = ? AND continent_code = ?", (event.name(), event.continent_code()))

            id_ = cursor.fetchone()

            event_list.append(p2app.events.continents.ContinentSearchResultEvent
                   (p2app.events.continents.Continent(id_[0], event.continent_code(),
                                                      event.name())))

        return event_list
    except Exception:
        pass

def load(event, cursor):
    """loads a continent from the database to edit it"""
    cursor.execute("SELECT * FROM continent WHERE continent_id = ?"
                        , (event.continent_id(),))
    row = cursor.fetchone()

    return (p2app.events.continents.ContinentLoadedEvent
           (p2app.events.continents.Continent(row[0], row[1], row[2])))

def update(event, cursor, conn):
    """saves a new continent into the database"""
    try:

        cursor.execute("UPDATE continent SET continent_code = ? , name = ? WHERE continent_id = ?",
                            (event.continent().continent_code, event.continent().name,
                             event.continent().continent_id))

        conn.commit()

        return (p2app.events.continents.ContinentSavedEvent(p2app.events.continents.Continent
                                                           (event.continent().continent_id,
                                                            event.continent().continent_code
                                                            , event.continent().name)))

    except Exception as e:
        return p2app.events.continents.SaveContinentFailedEvent(e)

def add_new(event, cursor, conn):
    """User saves a modified continent into the database"""
    try:
        cursor.execute("INSERT INTO continent (continent_id, continent_code, name)"
                            " VALUES (?, ?, ?)",
                            (event.continent().continent_id,
                             event.continent().continent_code,
                             event.continent().name,))

        conn.commit()

        cursor.execute("SELECT continent_id FROM continent "
                            "WHERE continent_code = ? AND name = ?",
                            (event.continent().continent_code,
                             event.continent().name))

        id_ = cursor.fetchone()
        return p2app.events.continents.ContinentSavedEvent(p2app.events.continents.Continent
                                                          (id_[0], event.continent().name,
                                                           event.continent().continent_code))

    except Exception as e:
        return p2app.events.continents.SaveContinentFailedEvent(e)