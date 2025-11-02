# This is 'modules/book_management.py'

from database.db_connection import create_connection, close_connection

def add_book(title, author, isbn, genre, quantity):
    """Adds a new book to the books table."""
    conn = create_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    
    # We set available_quantity to be the same as total quantity initially
    query = """
    INSERT INTO books (title, author, isbn, genre, quantity, available_quantity) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (title, author, isbn, genre, quantity, quantity))
        conn.commit()  # commit() is needed to save changes
        print(f"Success: Added '{title}' by {author}.")
        return True
    except Exception as e:
        print(f"Error adding book: {e}")
        conn.rollback() # Rollback changes on error
        return False
    finally:
        cursor.close()
        close_connection(conn)

def search_book(search_term):
    """Searches for books by title, author, or ISBN."""
    conn = create_connection()
    if not conn:
        return []
        
    cursor = conn.cursor(dictionary=True) # dictionary=True gives us results as dicts
    
    # Using LIKE with % allows for partial matches
    query = """
    SELECT * FROM books 
    WHERE title LIKE %s OR author LIKE %s OR isbn = %s
    """
    # We add '%' wildcards to the search term
    like_term = f"%{search_term}%"
    
    try:
        cursor.execute(query, (like_term, like_term, search_term))
        results = cursor.fetchall()
        
        if not results:
            print("No books found matching that criteria.")
        
        return results # Returns a list of dictionaries
        
    except Exception as e:
        print(f"Error searching for book: {e}")
        return [] # Return empty list on error
    finally:
        cursor.close()
        close_connection(conn)

def update_book_details(book_id, new_title, new_author, new_quantity):
    """Updates a book's details based on its book_id."""
    conn = create_connection()
    if not conn:
        return False

    cursor = conn.cursor()
    
    # This query is more complex, it needs to update available_quantity too
    query = """
    UPDATE books 
    SET title = %s, 
        author = %s, 
        quantity = %s,
        available_quantity = available_quantity + (%s - quantity) -- Adjust available count
    WHERE book_id = %s
    """
    try:
        cursor.execute(query, (new_title, new_author, new_quantity, new_quantity, book_id))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Success: Updated book ID {book_id}.")
            return True
        else:
            print(f"Notice: No book found with ID {book_id} to update.")
            return False
            
    except Exception as e:
        print(f"Error updating book: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        close_connection(conn)

def remove_book(book_id):
    """Removes a book from the database using its book_id."""
    conn = create_connection()
    if not conn:
        return False
        
    cursor = conn.cursor()
    query = "DELETE FROM books WHERE book_id = %s"
    
    try:
        cursor.execute(query, (book_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f"Success: Removed book ID {book_id}.")
            return True
        else:
            print(f"Notice: No book found with ID {book_id} to remove.")
            return False
            
    except Exception as e:
        print(f"Error removing book: {e}")
        print("Hint: You cannot remove a book that is currently issued to a member.")
        conn.rollback()
        return False
    finally:
        cursor.close()
        close_connection(conn)

# --- Test block ---
if __name__ == '__main__':
    print("--- Testing Book Management System ---")
    
    # 1. Add a new book
    print("\nAttempting to add 'The Great Gatsby'...")
    add_book('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 'Fiction', 5)
    
    print("\nAttempting to add 'Data Science 101'...")
    add_book('Data Science 101', 'John Doe', '1234567890123', 'Education', 3)

    # 2. Search for the book
    print("\nSearching for 'Gatsby'...")
    books = search_book('Gatsby')
    for book in books:
        print(f"  > Found: {book['title']} (ID: {book['book_id']})")

    # 3. Update the book (let's get the ID from the search)
    if books:
        book_id_to_update = books[0]['book_id']
        print(f"\nUpdating book ID {book_id_to_update}...")
        update_book_details(book_id_to_update, 'The Great Gatsby (Updated)', 'F. Scott Fitzgerald', 7)
        
        # Verify update
        print("  > Verifying update by searching again:")
        updated_books = search_book('Gatsby')
        for book in updated_books:
            print(f"  > Found: {book['title']}, Quantity: {book['quantity']}")
            
    # 4. Remove the book
    if books:
        book_id_to_remove = books[0]['book_id']
        print(f"\nAttempting to remove book ID {book_id_to_remove}...")
        remove_book(book_id_to_remove)
        
        # Verify removal
        print("  > Verifying removal by searching again:")
        removed_books = search_book('Gatsby')
        if not removed_books:
            print("  > Book successfully removed.")
            
    # 5. Test removing the other book
    print("\nSearching for 'Data Science 101' to get its ID...")
    ds_books = search_book('1234567890123') # Search by unique ISBN
    if ds_books:
        ds_book_id = ds_books[0]['book_id']
        print(f"  > Found book ID {ds_book_id}. Removing it...")
        remove_book(ds_book_id)