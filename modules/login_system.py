# This is 'modules/login_system.py'

import hashlib
# We need to import the connection functions from our database module
from database.db_connection import create_connection, close_connection

def hash_password(password):
    """Hashes a password using SHA-256 for secure storage."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_login(username, password):
    """Checks user credentials against the database."""
    
    # Hash the provided password to compare with the one in the DB
    hashed_pass_to_check = hash_password(password)
    
    conn = create_connection()
    if not conn:
        # This is a better error message
        print("Database connection failed. Check config and MySQL service.")
        return False 

    cursor = conn.cursor()
    
    # Use a parameterized query to prevent SQL injection
    query = "SELECT password_hash FROM users WHERE username = %s"
    
    try:
        cursor.execute(query, (username,))
        result = cursor.fetchone() # Get the first matching record
        
        if result:
            # result[0] contains the password_hash from the DB
            stored_password_hash = result[0] 
            
            if stored_password_hash == hashed_pass_to_check:
                print(f"Login successful. Welcome, {username}!")
                return True
            else:
                print("Invalid password.")
                return False
        else:
            print("Invalid username.")
            return False
            
    except Exception as e:
        print(f"An error occurred during login: {e}")
        return False
    finally:
        # Always close the cursor and connection
        cursor.close()
        close_connection(conn)

# --- Test block ---
# This code runs ONLY when you run this file directly
if __name__ == '__main__':
    print("--- Testing Login System ---")
    
    # Test 1: Successful Admin Login
    # (Remember we created 'admin' with password 'admin' in the SQL script)
    print("\nAttempting 'admin' with 'admin' (should work):")
    verify_login('admin', 'admin')

    # Test 2: Failed Login (Wrong Password)
    print("\nAttempting 'admin' with 'wrongpass' (should fail):")
    verify_login('admin', 'wrongpass')

    # Test 3: Failed Login (Wrong Username)
    print("\nAttempting 'notauser' with 'admin' (should fail):")
    verify_login('notauser', 'admin')