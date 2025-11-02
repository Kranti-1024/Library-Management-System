# This is 'modules/issue_return.py'

import datetime
from database.db_connection import create_connection, close_connection

def issue_book(book_id, member_id):
    """Issues a book to a member and creates a transaction record."""
    
    # Set issue date and a 14-day due date
    issue_date = datetime.date.today()
    due_date = issue_date + datetime.timedelta(days=14)
    
    conn = create_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    
    try:
        # 1. Check if the book is available
        cursor.execute("SELECT available_quantity FROM books WHERE book_id = %s", (book_id,))
        result = cursor.fetchone()
        
        if not result or result[0] <= 0:
            print(f"Error: Book ID {book_id} is not available for issue.")
            return False
            
        # 2. Decrement the book's available quantity
        update_book_query = "UPDATE books SET available_quantity = available_quantity - 1 WHERE book_id = %s"
        cursor.execute(update_book_query, (book_id,))
        
        # 3. Create the new transaction record
        insert_trans_query = """
        INSERT INTO transactions (book_id, member_id, issue_date, due_date, return_date, fine_amount)
        VALUES (%s, %s, %s, %s, NULL, 0.00)
        """
        cursor.execute(insert_trans_query, (book_id, member_id, issue_date, due_date))
        
        # If all steps succeeded, commit the changes
        conn.commit()
        print(f"Success: Book ID {book_id} issued to member ID {member_id}.")
        return True
        
    except Exception as e:
        # If any step fails, roll back all changes
        print(f"Error during book issue: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        close_connection(conn)

def return_book(book_id, member_id):
    """Returns a book, marks the transaction complete, and calculates fine."""
    
    conn = create_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    
    try:
        # 1. Find the OPEN transaction (where return_date is NULL)
        find_trans_query = """
        SELECT transaction_id, due_date FROM transactions 
        WHERE book_id = %s AND member_id = %s AND return_date IS NULL
        """
        cursor.execute(find_trans_query, (book_id, member_id))
        trans = cursor.fetchone()
        
        if not trans:
            print(f"Error: No active issue record found for book ID {book_id} and member ID {member_id}.")
            return False
            
        transaction_id = trans[0]
        due_date = trans[1]
        
        # 2. Calculate fine
        today = datetime.date.today()
        fine = 0.00
        if today > due_date:
            # We need the fine_per_day from config
            # Let's import it (or you can pass it as an argument)
            from utils.config import FINE_PER_DAY
            days_overdue = (today - due_date).days
            fine = days_overdue * FINE_PER_DAY
            
        # 3. Update the transaction with return date and fine
        update_trans_query = "UPDATE transactions SET return_date = %s, fine_amount = %s WHERE transaction_id = %s"
        cursor.execute(update_trans_query, (today, fine, transaction_id))
        
        # 4. Increment the book's available quantity
        update_book_query = "UPDATE books SET available_quantity = available_quantity + 1 WHERE book_id = %s"
        cursor.execute(update_book_query, (book_id,))
        
        # If all steps succeeded, commit
        conn.commit()
        print(f"Success: Book ID {book_id} returned by member ID {member_id}. Fine: {fine}")
        return True

    except Exception as e:
        print(f"Error during book return: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        close_connection(conn)

# --- Test block ---
if __name__ == '__main__':
    # We must import our other modules to create data for the test
    from modules.book_management import add_book, search_book, remove_book
    from modules.member_management import register_member, view_member_details
    # We will also need a way to remove members, let's add a quick helper
    
    def simple_remove_member(member_id):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM members WHERE member_id = %s", (member_id,))
        conn.commit()
        cursor.close()
        close_connection(conn)

    print("--- Testing Issue/Return System ---")
    
    # 1. Setup: Create a new book and a new member for this test
    print("\nSetting up test data...")
    add_book('Test Book for Issuing', 'Test Author', '999999999', 'Test', 1)
    register_member('Test Member', 'test@member.com', '5555555')
    
    # 2. Get their new IDs
    test_book = search_book('999999999')[0]
    test_member = view_member_details('test@member.com')[0]
    book_id = test_book['book_id']
    member_id = test_member['member_id']
    print(f"  > Created book ID {book_id} (Available: {test_book['available_quantity']})")
    print(f"  > Created member ID {member_id}")

    # 3. Issue the book
    print("\nIssuing the book...")
    issue_book(book_id, member_id)
    
    # 4. Check if quantity decreased
    book_after_issue = search_book('999999999')[0]
    print(f"  > Book quantity after issue: {book_after_issue['available_quantity']}") # Should be 0

    # 5. Try to issue again (should fail)
    print("\nIssuing the same book again (should fail)...")
    issue_book(book_id, member_id) # Should print an error
    
    # 6. Return the book
    print("\nReturning the book...")
    return_book(book_id, member_id)

    # 7. Check if quantity increased
    book_after_return = search_book('999999999')[0]
    print(f"  > Book quantity after return: {book_after_return['available_quantity']}") # Should be 1
    
    # 8. Clean up
    print("\nCleaning up test data...")
    # Must remove transactions first due to foreign key constraints
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE book_id = %s", (book_id,))
    conn.commit()
    cursor.close()
    close_connection(conn)
    
    remove_book(book_id)
    simple_remove_member(member_id)
    print("  > Cleanup complete.")