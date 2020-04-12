import sqlite3

conn = sqlite3.connect("furniture.sqlite")

c = conn.cursor()
c.execute(
    """
          DROP TABLE furniture
          """
)

conn.commit()
conn.close()
