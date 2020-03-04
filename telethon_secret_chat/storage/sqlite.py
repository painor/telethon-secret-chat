import datetime
import os

from .memory import SecretMemorySession

try:
    import sqlite3

    sqlite3_err = None
except ImportError as e:
    sqlite3 = None
    sqlite3_err = type(e)


class SQLiteSession(SecretMemorySession):
    """This session contains the required information to login into your
       Telegram account. NEVER give the saved session file to anyone, since
       they would gain instant access to all your messages and contacts.

       If you think the session has been compromised, close all the sessions
       through an official Telegram client to revoke the authorization.
    """

    def __init__(self, sqlite_connection):
        if sqlite3 is None:
            raise sqlite3_err
        if not isinstance(sqlite_connection, sqlite3.Connection):
            raise ConnectionError("Please pass an sqlite3 connection")
        super().__init__()
        self.filename = ':memory:'
        self.save_entities = True

        self._conn = None
        c = self._cursor()
        c.execute("select name from sqlite_master "
                  "where type='table' and name='secret_chats'")
        if c.fetchone():
            # Tables already exist, check for the version
            c.execute("select * from secret_chats")
            secret_chats = c.fetchall()
            c.close()
        else:
            # Tables don't exist, create new ones
            self._create_table(
                c,
                """plugin_secret_chats (
                  
                )"""
            )

            c.close()
            self.save()

    @staticmethod
    def _create_table(c, *definitions):
        for definition in definitions:
            c.execute('create table {}'.format(definition))

    def save(self):
        """Saves the current session object as session_user_id.session"""
        # This is a no-op if there are no changes to commit, so there's
        # no need for us to keep track of an "unsaved changes" variable.
        if self._conn is not None:
            self._conn.commit()

    def _cursor(self):
        """Asserts that the connection is open and returns a cursor"""
        if self._conn is None:
            self._conn = sqlite3.connect(self.filename,
                                         check_same_thread=False)
        return self._conn.cursor()

    def _execute(self, stmt, *values):
        """
        Gets a cursor, executes `stmt` and closes the cursor,
        fetching one row afterwards and returning its result.
        """
        c = self._cursor()
        try:
            return c.execute(stmt, values).fetchone()
        finally:
            c.close()

    def close(self):
        """Closes the connection unless we're working in-memory"""
        if self.filename != ':memory:':
            if self._conn is not None:
                self._conn.commit()
                self._conn.close()
                self._conn = None

    def delete(self):
        """Deletes the current session file"""
        if self.filename == ':memory:':
            return True
        try:
            os.remove(self.filename)
            return True
        except OSError:
            return False
