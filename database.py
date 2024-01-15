import sqlite3

def delete_car_listing(car_id):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('car_listings.db')
        cur = conn.cursor()

        # Execute the DELETE statement
        cur.execute("DELETE FROM cars WHERE id = ?", (car_id,))

        # Commit the changes
        conn.commit()

        if cur.rowcount == 0:
            print("No car found with ID:", car_id)
        else:
            print("Car listing deleted successfully")

    except sqlite3.Error as e:
        print("Error while deleting car listing:", e)
    finally:
        # Close the connection
        conn.close()


def insert_car_listing(make, model, year, price, mileage):
    conn = sqlite3.connect('car_listings.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO cars (make, model, year, price, mileage) VALUES (?, ?, ?, ?, ?)", 
                (make, model, year, price, mileage))
    conn.commit()
    conn.close()

def get_toyota_cars():
    conn = sqlite3.connect('car_listings.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM cars WHERE make='Toyota'")
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()


insert_car_listing('Toyota', 'Yaris', 2012, 9500, 100000)
get_toyota_cars()
delete_car_listing(1)
get_toyota_cars()
