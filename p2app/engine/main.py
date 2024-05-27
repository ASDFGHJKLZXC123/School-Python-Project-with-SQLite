# p2app/engine/main.py
#
# ICS 33 Spring 2024
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.

import p2app.events
import sqlite3
import p2app.engine.continents
import p2app.engine.countries
import p2app.engine.regions

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        pass


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        if isinstance(event, p2app.events.OpenDatabaseEvent):
            try:
                self.conn = sqlite3.connect(event.path())
                self.cursor = self.conn.cursor()
                required_tables = ['continent', 'country', 'region']
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
                tables = [row[0] for row in self.cursor.fetchall()]

                for table in required_tables:
                    if table not in tables:
                        yield p2app.events.DatabaseOpenFailedEvent(
                            "The File Doesn't Have Required Tables")

                yield p2app.events.DatabaseOpenedEvent(event.path())
            except Exception as e:
                yield p2app.events.DatabaseOpenFailedEvent(str(e))

        elif isinstance(event, p2app.events.QuitInitiatedEvent):
            yield p2app.events.EndApplicationEvent

        elif isinstance(event, p2app.events.CloseDatabaseEvent):
            yield p2app.events.DatabaseClosedEvent

        elif isinstance(event, p2app.events.continents.StartContinentSearchEvent):
            try:
                continent_search_event_list = p2app.engine.continents.search(event, self.cursor)
                for i in continent_search_event_list:
                    yield i
            except Exception:
                pass

        elif isinstance(event, p2app.events.continents.LoadContinentEvent):
            yield p2app.engine.continents.load(event, self.cursor)

        elif isinstance(event, p2app.events.continents.SaveContinentEvent):
            yield p2app.engine.continents.update(event, self.cursor, self.conn)

        elif isinstance(event, p2app.events.continents.SaveNewContinentEvent):
            yield p2app.engine.continents.add_new(event, self.cursor, self.conn)

        elif isinstance(event, p2app.events.countries.StartCountrySearchEvent):
            try:
                country_search_event_list = p2app.engine.countries.search(event, self.cursor)
                for i in country_search_event_list:
                    yield i
            except Exception:
                pass

        elif isinstance(event, p2app.events.countries.LoadCountryEvent):
            yield p2app.engine.countries.load(event, self.cursor)

        elif isinstance(event, p2app.events.countries.SaveNewCountryEvent):
            yield p2app.engine.countries.add_new(event, self.cursor, self.conn)

        elif isinstance(event, p2app.events.countries.SaveCountryEvent):
            yield p2app.engine.countries.update(event, self.cursor, self.conn)

        elif isinstance(event, p2app.events.regions.StartRegionSearchEvent):
            try:
                region_search_event_list = p2app.engine.regions.search(event, self.cursor)
                for i in region_search_event_list:
                    yield i
            except Exception:
                pass

        elif isinstance(event, p2app.events.regions.LoadRegionEvent):
            yield p2app.engine.regions.load(event, self.cursor)

        elif isinstance(event, p2app.events.regions.SaveNewRegionEvent):
            yield p2app.engine.regions.add_new(event, self.cursor, self.conn)

        elif isinstance(event, p2app.events.regions.SaveRegionEvent):
            yield p2app.engine.regions.update(event, self.cursor, self.conn)