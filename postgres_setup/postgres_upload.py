import csv
import psycopg2

# SQL to create the cars table if it doesn't exist
create_table_sql = """
CREATE TABLE IF NOT EXISTS cars (
    id SERIAL PRIMARY KEY,
    cost INTEGER,
    year INTEGER,
    make VARCHAR(50),
    model VARCHAR(50),
    mileage INTEGER,
    fuel_type VARCHAR(20),
    image_url TEXT
);
"""

# SQL to insert a new car record
insert_car_sql = """
INSERT INTO cars (cost, year, make, model, mileage, fuel_type, image_url)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""

def import_csv_to_db(csv_file_path):
    conn = None
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password",
            host="34.42.60.242",
            port=5432
        )
        cur = conn.cursor()
        print("Connected to the PostgreSQL database.")

        # Create the table if it doesn't exist
        cur.execute(create_table_sql)

        # Open and read the CSV file
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Extract data from CSV row
                cost = int(row['Cost'])
                year = int(row['Year'])
                make = row['Make']
                model = row['Model']
                mileage = int(row['Mileage'])
                fuel_type = row['Fuel Type']
                image_url = row['Image URL']

                # Insert data into the database
                cur.execute(insert_car_sql, (cost, year, make, model, mileage, fuel_type, image_url))

        # Commit the transaction
        conn.commit()
        print("Data import completed successfully.")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL or importing data:", error)
    finally:
        if conn:
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed.")

# Call the function with your CSV file path
import_csv_to_db('car_inventory.csv')