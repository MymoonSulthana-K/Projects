import mysql.connector
global cnx
# Establish a connection to the database
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123$$",
    database="ticketbooking"
)

def insert_ticket_details(ticket_id, name, category_id, show_id, date, total_price,quantity):
    cursor = cnx.cursor()

    # Fetch the price for the given category_id
    query = "SELECT price FROM category WHERE category_id = %s"
    cursor.execute(query, (category_id,))
    result = cursor.fetchone()

    if result is None:
        print(f"Category ID {category_id} does not exist.")
        cursor.close()
        return

    # Insert the ticket details into the ticket_details table
    insert_query = """
    INSERT INTO ticket_details (ticket_id, name, category_id, show_id, date, total_price, quantity)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (ticket_id, name, category_id, show_id, date, total_price, quantity)

    try:
        cursor.execute(insert_query, values)
        cnx.commit()  # Commit the transaction
        print("Ticket details inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()

# Example usage
#insert_ticket_details(ticket_id=2, name='Neha', category_id=102, show_id=202, date='2024-10-10', quantity=2)

def view_ticket_details(ticket_id):
    cursor = cnx.cursor()

    # Query to fetch ticket details by ticket_id
    query = "SELECT * FROM ticket_details WHERE ticket_id = %s"
    
    cursor.execute(query, (ticket_id,))
    result = cursor.fetchone()

    cursor.close()  # Ensure the cursor is closed after the operation
    return result

# Example usa
print(view_ticket_details(1))

def get_price_by_show_and_category(show_id, category_id):
    cursor = cnx.cursor()

    # Query to fetch the price based on show_id and category_id
    query = """
    SELECT s.price AS show_price, c.price AS category_price 
    FROM shows s
    JOIN category c ON c.category_id = %s
    WHERE s.show_id = %s
    """

    cursor.execute(query, (category_id, show_id))
    result = cursor.fetchone()
    total_price = result[0]+result[1]
    cursor.close()  # Ensure the cursor is closed after the operation

    # If result is None, it means the combination of show_id and category_id does not exist
    return total_price

print(get_price_by_show_and_category(201,101))