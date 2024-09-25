from dbconfig.dbconfig import MySqLConnectionCreator


def save_classification_to_db(road_id, road_name, latitud, longitud, L_danios):
    """
    Save road classification data to the database.

    Args:
        road_id (int): The road ID.
        road_name (str): The name of the road.
        latitud (float): The latitude of the road.
        longitud (float): The longitude of the road.
        L_danios (list): List of classifications to be stored as a comma-separated string.
    """
    # Convert the list of classifications to a comma-separated string
    classifications = ', '.join(L_danios)

    # Initialize the MySQL connection creator
    connector = MySqLConnectionCreator()
    conn = connector.db_conn

    if conn is not None:
        try:
            cursor = conn.cursor()

            # SQL query to insert the data into road_classification table
            query = """
            INSERT INTO road_classification (road_id, road_name, classifications, location_lat, location_lon)
            VALUES (%s, %s, %s, %s, %s)
            """
            
            # Execute the query with provided parameters
            cursor.execute(query, (road_id, road_name, classifications, latitud, longitud))

            # Commit the transaction
            conn.commit()
            print(f"Data for road {road_name} saved successfully.")

        except Error as e:
            print(f"Failed to insert record into MySQL table: {e}")

        finally:
            # Close the cursor and the database connection
            cursor.close()
            connector.close_db_connection(conn)
    else:
        print("Connection to the database failed.")
