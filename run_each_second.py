import time
import pandas_gbq
import psycopg2
import json



def connect_and_read_vendors():
    """ Connect to the PostgreSQL database server and read vendors """
    connection = None
    try:
        # Connect to your postgres DB
        connection = psycopg2.connect(
            host="localhost",  # Or another hostname if not local
            database="mms",  # Your database name
            user="postgres",  # Your database username
            password="admin"  # Your database password
        )

        # Create a cursor object
        cursor = connection.cursor()

        # Execute a query
        cursor.execute("SELECT * FROM mms_api_vendor limit 1")

        # Fetch and print the result of the query
        vendor_records = cursor.fetchall()
        # Get column headers
        columns = [desc[0] for desc in cursor.description]

        # Convert query to json
        result = []
        for row in vendor_records:
            record = dict(zip(columns, row))
            result.append(record)

        # Convert list of dicts to JSON string
        json_result = json.dumps(result,default=str)  # default=str to handle datetime and other non-serializable types

        print(json_result)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        cursor.close()
        connection.close()



# def fetch_and_insert_vendors():
#     query = f"""
#         SELECT id,enName,arName  from `food_prod_public.vendors limit 1`
#        """
#     df = pandas_gbq.read_gbq(query, project_id='peak-brook-355811')
#     print(df)

connect_and_read_vendors()
# Main loop
# while True:
#     connect_and_read_vendors()
#
#     time.sleep(86400)  # Sleep for 1 second before running the function again
