import sqlite3

conn = sqlite3.connect("furniture.sqlite")

c = conn.cursor()
c.execute(
    """
          CREATE TABLE furniture
          (id INTEGER PRIMARY KEY ASC,
           type VARCHAR(4) NOT NULL,
           item_serial_number VARCHAR(100) NOT NULL,
           year_manufactured VARCHAR(4) NOT NULL,
           item_brand VARCHAR(20) NOT NULL,
           price FLOAT NOT NULL,
           cost FLOAT NOT NULL,
           size VARCHAR(20),
           height VARCHAR(20),
           number_of_cushions INTEGER,
           number_of_seats INTEGER,
           is_sold INTEGER NOT NULL)
          """
)

conn.commit()
conn.close()
