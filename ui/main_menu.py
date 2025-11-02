# This is the new 'ui/main_menu.py'

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Import all your backend modules just like before
from modules import login_system, book_management, member_management, issue_return

# --- Main Application Window ---

def launch_main_window():
    """Creates the main library application window after login."""
    
    main_app = tk.Tk()
    main_app.title("Library Management System")
    main_app.geometry("800x600")

    # Create a Tabbed Interface
    notebook = ttk.Notebook(main_app)
    
    # --- Tab 1: Book Management ---
    book_tab = ttk.Frame(notebook, padding="10")
    notebook.add(book_tab, text='Book Management')
    create_book_tab(book_tab)
    
    # --- Tab 2: Member Management ---
    member_tab = ttk.Frame(notebook, padding="10")
    notebook.add(member_tab, text='Member Management')
    create_member_tab(member_tab)

    # --- Tab 3: Issue/Return ---
    issue_tab = ttk.Frame(notebook, padding="10")
    notebook.add(issue_tab, text='Issue/Return Books')
    create_issue_return_tab(issue_tab)

    notebook.pack(expand=True, fill='both')
    main_app.mainloop()

# --- Functions to create each tab ---

def create_book_tab(tab):
    """Populates the Book Management tab with widgets."""
    
    # Frame for buttons
    btn_frame = ttk.Frame(tab)
    btn_frame.pack(pady=10, fill='x')

    ttk.Button(btn_frame, text="Add New Book", command=add_book_popup).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Search Books", command=lambda: search_book_gui(tree)).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Remove Selected Book", command=lambda: remove_book_gui(tree)).pack(side=tk.LEFT, padx=5)

    # Treeview to display search results
    cols = ('Book ID', 'Title', 'Author', 'ISBN', 'Genre', 'Available', 'Total')
    tree = ttk.Treeview(tab, columns=cols, show='headings')
    
    for col in cols:
        tree.heading(col, text=col)
    
    tree.pack(expand=True, fill='both')

def create_member_tab(tab):
    """Populates the Member Management tab with widgets."""
    
    # Frame for buttons
    btn_frame = ttk.Frame(tab)
    btn_frame.pack(pady=10, fill='x')

    ttk.Button(btn_frame, text="Register New Member", command=add_member_popup).pack(side=tk.LEFT, padx=5)
    ttk.Button(btn_frame, text="Search Members", command=lambda: search_member_gui(tree)).pack(side=tk.LEFT, padx=5)

    # Treeview to display search results
    cols = ('Member ID', 'Name', 'Email', 'Phone', 'Reg. Date')
    tree = ttk.Treeview(tab, columns=cols, show='headings')
    
    for col in cols:
        tree.heading(col, text=col)
    
    tree.pack(expand=True, fill='both')

def create_issue_return_tab(tab):
    """Populates the Issue/Return tab with widgets."""
    
    form_frame = ttk.Frame(tab, padding="10")
    form_frame.pack(pady=20)

    ttk.Label(form_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    book_id_entry = ttk.Entry(form_frame, width=30)
    book_id_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Member ID:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
    member_id_entry = ttk.Entry(form_frame, width=30)
    member_id_entry.grid(row=1, column=1, padx=5, pady=5)
    
    btn_frame = ttk.Frame(tab)
    btn_frame.pack(pady=10)

    def issue_gui():
        book_id = book_id_entry.get()
        member_id = member_id_entry.get()
        if not book_id or not member_id:
            messagebox.showwarning("Input Error", "Book ID and Member ID are required.")
            return
        
        # We call your existing backend function!
        if issue_return.issue_book(int(book_id), int(member_id)):
            messagebox.showinfo("Success", f"Book ID {book_id} issued to member ID {member_id}.")
            book_id_entry.delete(0, tk.END)
            member_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to issue book. Check availability or inputs.")

    def return_gui():
        book_id = book_id_entry.get()
        member_id = member_id_entry.get()
        if not book_id or not member_id:
            messagebox.showwarning("Input Error", "Book ID and Member ID are required.")
            return

        # We call your existing backend function!
        if issue_return.return_book(int(book_id), int(member_id)):
            messagebox.showinfo("Success", f"Book ID {book_id} returned by member ID {member_id}.")
            book_id_entry.delete(0, tk.END)
            member_id_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to return book. Check inputs.")

    ttk.Button(btn_frame, text="Issue Book", command=issue_gui).pack(side=tk.LEFT, padx=10, ipady=5)
    ttk.Button(btn_frame, text="Return Book", command=return_gui).pack(side=tk.LEFT, padx=10, ipady=5)


# --- Pop-up Window Functions (for Forms) ---

def add_book_popup():
    """Creates a pop-up form to add a new book."""
    popup = tk.Toplevel()
    popup.title("Add New Book")
    
    # Simple form
    frame = ttk.Frame(popup, padding="15")
    frame.pack()
    
    fields = ['Title', 'Author', 'ISBN', 'Genre', 'Quantity']
    entries = {}
    for i, field in enumerate(fields):
        ttk.Label(frame, text=f"{field}:").grid(row=i, column=0, sticky='w', padx=5, pady=5)
        entry = ttk.Entry(frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[field] = entry

    def submit():
        try:
            # We call your existing backend function!
            book_management.add_book(
                title=entries['Title'].get(),
                author=entries['Author'].get(),
                isbn=entries['ISBN'].get(),
                genre=entries['Genre'].get(),
                quantity=int(entries['Quantity'].get())
            )
            messagebox.showinfo("Success", "Book added successfully!")
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {e}")

    ttk.Button(frame, text="Submit", command=submit).grid(row=len(fields), columnspan=2, pady=10)

def add_member_popup():
    """Creates a pop-up form to register a new member."""
    popup = tk.Toplevel()
    popup.title("Register New Member")
    
    frame = ttk.Frame(popup, padding="15")
    frame.pack()
    
    fields = ['Name', 'Email', 'Phone Number']
    entries = {}
    for i, field in enumerate(fields):
        ttk.Label(frame, text=f"{field}:").grid(row=i, column=0, sticky='w', padx=5, pady=5)
        entry = ttk.Entry(frame, width=40)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries[field] = entry
    
    def submit():
        try:
            # We call your existing backend function!
            member_management.register_member(
                name=entries['Name'].get(),
                email=entries['Email'].get(),
                phone_number=entries['Phone Number'].get()
            )
            messagebox.showinfo("Success", "Member registered successfully!")
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register member: {e}")

    ttk.Button(frame, text="Register", command=submit).grid(row=len(fields), columnspan=2, pady=10)

# --- GUI Helper Functions (connecting buttons to backend) ---

def search_book_gui(tree):
    """Prompts for search term and displays results in the Treeview."""
    term = simpledialog.askstring("Search", "Enter Title, Author, or ISBN:")
    if not term:
        return
        
    # Clear old results
    for item in tree.get_children():
        tree.delete(item)
        
    # We call your existing backend function!
    results = book_management.search_book(term)
    
    # Populate the tree
    for book in results:
        tree.insert('', tk.END, values=(
            book['book_id'],
            book['title'],
            book['author'],
            book['isbn'],
            book['genre'],
            book['available_quantity'],
            book['quantity']
        ))

def remove_book_gui(tree):
    """Removes the book selected in the Treeview."""
    selected_item = tree.focus() # Get selected item
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a book from the list to remove.")
        return
        
    # Get book ID from the selected row (it's the first value)
    book_id = tree.item(selected_item)['values'][0]
    
    if messagebox.askyesno("Confirm", f"Are you sure you want to remove book ID {book_id}?"):
        # We call your existing backend function!
        if book_management.remove_book(book_id):
            messagebox.showinfo("Success", f"Book ID {book_id} removed.")
            tree.delete(selected_item) # Remove from view
        else:
            messagebox.showerror("Error", "Failed to remove book. (Is it currently issued?)")

def search_member_gui(tree):
    """Prompts for search term and displays member results."""
    term = simpledialog.askstring("Search", "Enter Name or Email:")
    if not term:
        return
        
    for item in tree.get_children():
        tree.delete(item)
        
    results = member_management.view_member_details(term)
    
    for member in results:
        tree.insert('', tk.END, values=(
            member['member_id'],
            member['name'],
            member['email'],
            member['phone_number'],
            member['registration_date']
        ))


# --- Login Window ---

def start_application():
    """Starts the application by showing the login window."""
    
    login_window = tk.Tk()
    login_window.title("LMS Login")
    login_window.geometry("300x150")
    
    frame = ttk.Frame(login_window, padding="10")
    frame.pack(expand=True)

    ttk.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
    username_entry = ttk.Entry(frame)
    username_entry.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    password_entry = ttk.Entry(frame, show="*") # Hides password
    password_entry.grid(row=1, column=1, padx=5, pady=5)

    def handle_login():
        username = username_entry.get()
        password = password_entry.get()
        
        # We call your existing login function!
        if login_system.verify_login(username, password):
            login_window.destroy() # Close login window
            launch_main_window() # Open main app
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    ttk.Button(frame, text="Login", command=handle_login).grid(row=2, columnspan=2, pady=10)
    
    login_window.mainloop()

# Note: The 'if __name__ == "__main__":' block is in main.py
# This file (main_menu.py) only needs to EXPORT the start_application function.