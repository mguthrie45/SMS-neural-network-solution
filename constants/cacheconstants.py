DBPATH = 'C:\spring22\data\cache\enccache.db'

#MAKE SURE ONE OF THE CATEGORIES is 'invalid'
CATEGORIES = ['invalid', 'shipping/order', 'discount', 'stop', 'misc/help', 'products']
INVIDX = 0
NUMCATEGORIES = len(CATEGORIES)

TABLENAMEQUERY = "SELECT name FROM sqlite_master WHERE type='table'"
CREATETABLEQUERY = lambda name: f"CREATE TABLE {name} (id integer PRIMARY KEY, msg text NOT NULL, label integer, encoding text);"
ADDROWQUERY = lambda table, msg, label, enc: f'INSERT INTO {table}(msg, label, encoding) VALUES ("{msg}", {label}, "{enc}")'
UPDATEROWBYIDQUERY = lambda table, msg, label, enc, id: f'UPDATE {table} SET msg="{msg}", label={label}, encoding="{enc}" WHERE id = {id}'
UPDATEROWBYMSGQUERY = lambda table, umsg, rmsg, label, enc: f'UPDATE {table} SET msg="{rmsg}", label={label}, encoding="{enc}" WHERE msg = "{umsg}"'
GETALLROWSQUERY = lambda table: f"SELECT * FROM {table};"
DELETECONTENTBYTABLEQUERY = lambda table: f"DELETE FROM {table};"

ROWMISMATCHERROR = lambda nrows, arows: f"addRowError: Tried to add {nrows} but added {arows} to database."