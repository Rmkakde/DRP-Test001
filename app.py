from flask import Flask, request, render_template_string
import pyodbc
import os

app = Flask(__name__)

# Take data in html form
form_html = '''
 <form method="POST">
 Name: <input type="text" name="name" required><br><br>
 Number: <input type="text" name="number" required><br><br>
 <input type="submit" value="Submit">
 </form>
'''

# create table if not alredy present
def create_table_if_not_exists(db_connection):
    cursor = db_connection.cursor()
    create_table_query = '''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='paasresource' AND xtype='U')
    BEGIN
    CREATE TABLE paasresource (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100),
    number NVARCHAR(50)
    );
    END
    '''
    cursor.execute(create_table_query)
    db_connection.commit()

@app.route('/', methods=['GET', 'POST'])
def connect_db():
    db_connection = None  # Initialize db_connection as None
    connection_status = "Not connected to the database"  # Default message

    # Check bd connection
    try:
        connection_string = os.getenv('DATABASE_URL') 
        print(f"Connection string: {connection_string}") 
        db_connection = pyodbc.connect(connection_string)
        connection_status = "Successfully connected to the database!"  # Successful yehhh!!
    except pyodbc.Error as err:
        connection_status = f"Failed to connect to database: {err}"  # Show error messsag
    except Exception as e:
        connection_status = f"An unexpected error occurred while connecting: {str(e)}"

    if request.method == 'POST' and db_connection:
        name = request.form['name']
        number = request.form['number']

        print(f"Received Name: {name}, Number: {number}")

        try:
            # Create the table if not present
            create_table_if_not_exists(db_connection)

            # Create cursor object
            cursor = db_connection.cursor()

            # SQL query to insert data into the database
            cursor.execute("INSERT INTO paasresource (name, number) VALUES (?, ?)", (name, number))

            # Commit the transaction
            db_connection.commit()

            # Return success messageee
            return f"Data inserted successfully!<br><br>Name: {name}, Number: {number}"

        except pyodbc.Error as err:
            return f"Database connection or query error: {err}"

        except Exception as e:
            return f"An unexpected error occurred: {str(e)}"

        finally:
            # Close the connection if it was successfully created
            if db_connection:
                db_connection.close()

    # If GET request, render the form along with connection status
    return render_template_string(form_html + f"<p>{connection_status}</p>")

if __name__ == '__main__':
    app.run(debug=True)
