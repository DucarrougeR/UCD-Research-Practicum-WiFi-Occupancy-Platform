# CONNECTION
conn = sqlite3.connect("TimeTable.db") # Connect to database (creates if it does not exist)
cursor = conn.cursor()

# Create a new table in the current database
# Specify column names and data types
cursor.execute("CREATE TABLE IF NOT EXISTS TimeTable ( ... )")
               # replace ... with
               # the Name for all columns of data to add to tables as follows
               # ClassRoom text, Occupancy integer, Full boolean, Empty boolean...


conn.commit() # Save the changes

# INSERTION
# source: http://flask.pocoo.org/snippets/37/
def insert(table, fields=(), values=()):
    # g.db is the database connection
    cur = g.db.cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    g.db.commit()
    id = cur.lastrowid
    cur.close()
    return id



# Handling multiple sub-requests in a single Flask request
# http://flask.pocoo.org/snippets/131/