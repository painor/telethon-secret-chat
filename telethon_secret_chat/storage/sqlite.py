from telethon.tl.types import InputEncryptedChat

from telethon_secret_chat.secret_methods import SecretChat
from .memory import SecretMemorySession

try:
    import sqlite3

    sqlite3_err = None
except ImportError as e:
    sqlite3 = None
    sqlite3_err = type(e)

TABLE_NAME = "plugin_secret_chats"


class SecretSQLiteSession(SecretMemorySession):
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

        self._conn = sqlite_connection
        c = self._conn.cursor()
        c.execute("select name from sqlite_master "
                  f"where type='table' and name='{TABLE_NAME}'")
        if not c.fetchone():
            # Tables don't exist, create new ones
            self._create_table(
                c,
                f"""{TABLE_NAME} (
                  id integer NOT NULL PRIMARY KEY,
                  access_hash integer,
                  auth_key blob,
                  admin integer,
                  user_id integer,
                  in_seq_no_x integer,
                  out_seq_no_x integer,
                  in_seq_no integer,
                  out_seq_no integer,
                  layer integer,
                  ttl integer,
                  ttr integer,
                  updated integer,
                  created integer,
                  mtproto integer,
                  temp integer
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

    def _execute(self, stmt, *values):
        """
        Gets a cursor, executes `stmt` and closes the cursor,
        fetching one row afterwards and returning its result.
        """
        c = self._conn.cursor()
        try:
            return c.execute(stmt, values).fetchone()
        finally:
            c.close()

    def close(self):
        """Closes the connection unless we're working in-memory"""
        if self._conn is not None:
            self._conn.commit()
            self._conn.close()
            self._conn = None

    def save_chat(self, chat: SecretChat, temp=False):
        c = self._conn.cursor()
        row = (
            chat.id, chat.access_hash, chat.auth_key, 1 if chat.admin else 0, chat.user_id, chat.in_seq_no_x,
            chat.out_seq_no_x, chat.in_seq_no, chat.out_seq_no, chat.layer, chat.ttl, chat.ttr, chat.updated,
            chat.created, chat.mtproto, temp)
        try:
            c.execute(
                f'insert or replace into {TABLE_NAME} values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', row)
            self.save()
        finally:
            c.close()

    def get_temp_secret_chat_by_id(self, id):
        row = self._execute(
            f"select * from {TABLE_NAME} where temp=1 and id = ? or user_id=?", id, id)
        if row:
            input_chat = InputEncryptedChat(chat_id=row[0], access_hash=row[1])
            return SecretChat(id=row[0], access_hash=row[1], auth_key=row[2], admin=True if row[3] else False,
                              user_id=row[4], in_seq_no_x=row[5], out_seq_no_x=row[6], in_seq_no=row[7],
                              out_seq_no=row[8], layer=row[9], ttl=row[10], ttr=row[11], updated=row[12],
                              created=row[13], mtproto=row[14], input_chat=input_chat, session=self, is_temp=True)

    def get_secret_chat_by_id(self, id):
        row = self._execute(
            f"select * from {TABLE_NAME} where temp=0 and id = ? or user_id = ? ORDER BY UPDATED", id, id)

        if row:
            input_chat = InputEncryptedChat(chat_id=row[0], access_hash=row[1])
            return SecretChat(id=row[0], access_hash=row[1], auth_key=row[2], admin=True if row[3] else False,
                              user_id=row[4], in_seq_no_x=row[5], out_seq_no_x=row[6], in_seq_no=row[7],
                              out_seq_no=row[8], layer=row[9], ttl=row[10], ttr=row[11], updated=row[12],
                              created=row[13], mtproto=row[14], input_chat=input_chat, session=self)

    def remove_secret_chat_by_id(self, id, temp=False):
        print("removing chat with id", id, "and is ", temp)
        c = self._conn.cursor()
        try:
            c.execute(f"delete from {TABLE_NAME} where id=? or user_id=? and temp=?", (id, id, 1 if temp else 0))
        finally:
            c.close()
