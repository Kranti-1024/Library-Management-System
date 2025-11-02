# This is 'modules/member_management.py'

import datetime
from database.db_connection import create_connection, close_connection

def register_member(name, email, phone_number):
    """Registers a new member in the members table."""
    conn = create_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    
    # Get today's date for the registration_date
    reg_date = datetime.date.today()
    
    query = """
    INSERT INTO members (name, email, phone_number, registration_date) 
    VALUES (%s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (name, email, phone_number, reg_date))
        conn.commit()
        print(f"Success: Registered new member '{name}' with email '{email}'.")
        return True
    except Exception as e:
        print(f"Error registering member: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        close_connection(conn)

def view_member_details(search_term):
    """Searches for a member by name or email."""
    conn = create_connection()
    if not conn:
        return []
        
    cursor = conn.cursor(dictionary=True) # Get results as dictionaries
    
    query = """
    SELECT member_id, name, email, phone_number, registration_date 
    FROM members 
    WHERE name LIKE %s OR email LIKE %s
    """
    like_term = f"%{search_term}%"
    
    try:
        cursor.execute(query, (like_term, like_term))
        results = cursor.fetchall()
        
        if not results:
            print("No members found matching that criteria.")
        
        return results # Returns a list of dictionaries
        
    except Exception as e:
        print(f"Error searching for member: {e}")
        return []
    finally:
        cursor.close()
        close_connection(conn)

# --- Test block ---
if __name__ == '__main__':
    print("--- Testing Member Management System ---")
    
    # 1. Register a new member
    print("\nAttempting to register 'Alice Smith'...")
    register_member('Alice Smith', 'alice@example.com', '1234567890')
    
    print("\nAttempting to register 'Bob Johnson'...")
    register_member('Bob Johnson', 'bob@example.com', '0987654321')

    # 2. Search for the member
    print("\nSearching for 'alice@example.com'...")
    members = view_member_details('alice@example.com')
    for member in members:
        print(f"  > Found: {member['name']} (ID: {member['member_id']})")

    # 3. Clean up (Optional, but good for testing)
    # We don't have a 'remove_member' yet, so we'll just test adding/viewing.
    # To properly clean up, we would need a delete function.
    
    print("\nSearching for 'Bob'...")
    bob_members = view_member_details('Bob')
    for member in bob_members:
        print(f"  > Found: {member['name']} (ID: {member['member_id']})")
    