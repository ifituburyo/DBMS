
import os
import sys
import psycopg2
from dotenv import load_dotenv
from flask import Flask, flash, request, jsonify, render_template, redirect

load_dotenv()
url = os.getenv('DATABASE_URL')
connection = psycopg2.connect(url)


app = Flask(__name__)

@app.get('/')
def home():
    return  render_template('main.html')  # No need to use './' in the path

## create the function that read the tables from the database
@app.route('/tables', methods=['GET'])
def tables():
    try:
        cursor = connection.cursor()
        # Change 'my_schema' to the schema you want to query
        cursor.execute("SELECT table_name, table_schema FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';")
        tables = cursor.fetchall()
        cursor.close()
        return render_template('tables.html', tables=tables)
    except Exception as e:
        return f"Error fetching tables: {str(e)}"
if __name__ == "__main__":
    app.run(debug=True)

    # implement add pig and remove pig in the records 
    # implement add pig and remove pig in the records
@app.route('/add_pig', methods=['GET', 'POST'])
def add_pig():
    if request.method == 'POST':
        # Get form data from the user
        tag_number = request.form['tag_number']
        breed = request.form['breed']
        birth_date = request.form['birth_date']
        gender = request.form['gender']
        current_weight = request.form['current_weight']
        pen_location = request.form['pen_location']
        
        # Insert the new pig into the pigs table
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO Pigs (tag_number, breed, birth_date, gender, current_weight, pen_location)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (tag_number, breed, birth_date, gender, current_weight, pen_location)
        )
        connection.commit()
        cursor.close()
        
        # Redirect to the list of pigs or success page
        return redirect('/pigs')
    # If it's a GET request, render the form
        return render_template('add_pig.html')
    elif request.method == 'GET':
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM pigs;")
        pigs = cursor.fetchall()
        cursor.close()
        return render_template('add_pig.html', pigs=pigs)
    

    
### managic landing page buttoms
@app.route('/manage_pigs', methods=['GET'])
def manage_pigs():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Pigs;")  # Adjust as necessary to fetch the required data
    pigs = cursor.fetchall()
    cursor.close()
    return render_template('manage_pigs.html', pigs=pigs)

@app.route('/manage_employees', methods=['GET'])
def manage_employees():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Employees;")  # Adjust as necessary
    employees = cursor.fetchall()
    cursor.close()
    return render_template('manage_employees.html', employees=employees)


@app.route('/manage_feed', methods=['GET'])
def manage_feed():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM feeding;")  # Adjust as necessary
    feed = cursor.fetchall()
    cursor.close()
    return render_template('manage_feeds.html', feed=feed)

@app.route('/manage_health', methods=['GET'])
def manage_health():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Healthcare;")  # Adjust as necessary
    health_records = cursor.fetchall()
    cursor.close()
    return render_template('manage_health.html', health_records=health_records)

# @app.route('/manage_sales', methods=['GET'])
# def manage_sales():
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM Sales;")  # Adjust as necessary
#     sales = cursor.fetchall()
#     cursor.close()
#     return render_template('manage_sales.html', sales=sales)
@app.route('/manage_sales', methods=['GET'])
def manage_sales():
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Sales;")
    sales = cursor.fetchall()
    cursor.close()
    return render_template('manage_sales.html', sales=sales)


@app.route('/complete_feeding/<int:schedule_id>', methods=['POST'])
def complete_feeding(schedule_id):
    cursor = connection.cursor()
    
    # Mark the feeding as completed and update the stock
    cursor.execute("UPDATE Feeding_Schedule SET status = 'Completed' WHERE schedule_id = %s", (schedule_id,))
    connection.commit()

    # Fetch updated feed stock after feeding is completed
    cursor.execute("""
        SELECT fs.feed_type, fs.quantity_in_stock 
        FROM Feed_Stock fs
        JOIN Feeding_Schedule sch ON fs.feed_id = sch.feed_id
        WHERE sch.schedule_id = %s
    """, (schedule_id,))
    
    stock = cursor.fetchone()
    
    if stock['quantity_in_stock'] < 50:  # Assuming 50 is a critical threshold
        flash(f"Warning: Feed stock for {stock['feed_type']} is running low ({stock['quantity_in_stock']} kg left). Please replenish soon.", "warning")
    
    cursor.close()
    
    return redirect('/feed_schedules')


@app.route('/feed_schedules', methods=['GET'])
def feed_schedules():
    cursor = connection.cursor()
    cursor.execute("""
        
        SELECT * FROM feeding_schedule
    """)
    
    schedules = cursor.fetchall()
    cursor.close()
    
    return render_template('feed_schedules.html', schedules=schedules)




########################################################Post features===================== 

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        role = request.form['role']
        contact_number = request.form['contact_number']
        
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO Employees (first_name, last_name, role, contact_number)
            VALUES (%s, %s, %s, %s);
        """, (first_name, last_name, role, contact_number))
        connection.commit()
        cursor.close()
        
        return redirect('/manage_employees')

    return render_template('add_employee.html')


@app.route('/add_pig_sale', methods=['POST'])
def add_pig_sale():
    # Retrieve the form data
    pig_id = request.form['pig_id']
    sale_date = request.form['sale_date']
    buyer_name = request.form['buyer_name']
    sale_price = request.form['sale_price']
    weight_at_sale = request.form['weight_at_sale']
    
    cursor = connection.cursor()
    
    try:
        # Check if the pig exists in the Pigs table
        cursor.execute("SELECT * FROM Pigs WHERE pig_id = %s;", (pig_id,))
        pig = cursor.fetchone()
        
        if not pig:
            flash(f"Pig ID {pig_id} not found!", "error")
            return redirect('/add_pig_sale')  # Redirect back to the form

        # Insert sale into Sales table
        cursor.execute("""
            INSERT INTO Sales (pig_id, sale_date, buyer_name, sale_price, weight_at_sale)
            VALUES (%s, %s, %s, %s, %s);
        """, (pig_id, sale_date, buyer_name, sale_price, weight_at_sale))

        # Delete the pig from the Pigs table
        cursor.execute("DELETE FROM Pigs WHERE pig_id = %s;", (pig_id,))
        
        # Commit the transaction
        connection.commit()
        flash(f"Pig ID {pig_id} sold successfully!", "success")
    
    except Exception as e:
        connection.rollback()  # Rollback the transaction in case of any error
        flash(f"Error: {str(e)}", "error")
    
    finally:
        cursor.close()

    return redirect('/manage_sales')
    return render_template('add_pigs.html')