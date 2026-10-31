import tkinter as tk
from tkinter import ttk, messagebox

class Book:
    def __init__(self, book_id, title, author, genre, total_quantity=1):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.total_quantity = total_quantity
        self.available_quantity = total_quantity
        self.borrowed_quantity = 0

    def check_availability(self):
        return self.available_quantity > 0

    def update_availability(self, status):
        self.available_quantity = self.total_quantity if status else 0
        self.borrowed_quantity = self.total_quantity - self.available_quantity

    def display_details(self):
        status = f"Available: {self.available_quantity}/{self.total_quantity}"
        return (
            f"Book ID: {self.book_id}\n"
            f"Title: {self.title}\n"
            f"Author: {self.author}\n"
            f"Genre: {self.genre}\n"
            f"Status: {status}\nBorrowed copies: {self.borrowed_quantity}"
        )


class FictionBook(Book):
    def __init__(self, book_id, title, author, genre, subgenre, total_quantity=1):
        super().__init__(book_id, title, author, genre, total_quantity)
        self.subgenre = subgenre

    def display_details(self):
        return super().display_details() + f"\nSubgenre: {self.subgenre}"


class NonFictionBook(Book):
    def __init__(self, book_id, title, author, genre, subject, total_quantity=1):
        super().__init__(book_id, title, author, genre, total_quantity)
        self.subject = subject

    def display_details(self):
        return super().display_details() + f"\nSubject: {self.subject}"


class ReferenceBook(Book):
    def __init__(self, book_id, title, author, genre, reference_type, total_quantity=1):
        super().__init__(book_id, title, author, genre, total_quantity)
        self.reference_type = reference_type

    def display_details(self):
        return super().display_details() + f"\nReference type: {self.reference_type}"


# -------------------- LIBRARY CATALOG --------------------

class LibraryCatalog:
    def __init__(self):
        self.books = []

    def find_book(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def add_book(self, book):
        if self.find_book(book.book_id):
            return False, "A book with this ID already exists."
        self.books.append(book)
        return True, "Book added successfully."

    def remove_book(self, book_id):
        book = self.find_book(book_id)
        if book is None:
            return False, "Book not found."
        if book.borrowed_quantity > 0:
            return False, "Some copies are borrowed. Return all borrowed copies before removing this book."
        self.books.remove(book)
        return True, "Book removed successfully."

    def search_books(self, keyword=""):
        keyword = keyword.strip().lower()
        if not keyword:
            return self.books[:]
        return [
            book for book in self.books
            if keyword in book.title.lower()
            or keyword in book.author.lower()
            or keyword in str(book.book_id).lower()
            or keyword in book.genre.lower()
        ]

    def borrow_book(self, book_id, quantity=1):
        book = self.find_book(book_id)
        if book is None:
            return False, "Book not found. Please check the Book ID."
        if quantity <= 0:
            return False, "Quantity must be at least 1."
        if book.available_quantity < quantity:
            if book.available_quantity == 0:
                return False, f'"{book.title}" is already fully borrowed.'
            return False, (f'Only {book.available_quantity} cop(y/ies) of '
                           f'"{book.title}" are available.')
        book.available_quantity -= quantity
        book.borrowed_quantity += quantity
        return True, (f'Successfully borrowed {quantity} cop(y/ies) of '
                      f'"{book.title}".')

    def return_book(self, book_id, quantity=1):
        book = self.find_book(book_id)
        if book is None:
            return False, "Book not found. Please check the Book ID."
        if quantity <= 0:
            return False, "Quantity must be at least 1."
        if book.borrowed_quantity < quantity:
            return False, f'Only {book.borrowed_quantity} borrowed cop(y/ies) can be returned.'
        book.borrowed_quantity -= quantity
        book.available_quantity += quantity
        return True, f'Successfully returned {quantity} cop(y/ies) of "{book.title}".'

    def available_books(self):
        return [book for book in self.books if book.check_availability()]


# -------------------- TKINTER GUI --------------------

class LibraryApp:
    BG = "#F3F6FB"
    NAVY = "#172554"
    BLUE = "#2563EB"
    WHITE = "#FFFFFF"
    TEXT = "#1E293B"
    MUTED = "#64748B"
    GREEN = "#15803D"
    RED = "#B91C1C"

    def __init__(self, root):
        self.root = root
        self.root.title("Library Catalog System")
        self.root.geometry("1180x720")
        self.root.minsize(980, 620)
        self.root.configure(bg=self.BG)

        self.library = LibraryCatalog()
        self.selected_book_id = None

        self.setup_styles()
        self.add_sample_books()
        self.build_layout()
        self.refresh_table()

    def setup_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background=self.WHITE,
            foreground=self.TEXT,
            rowheight=32,
            fieldbackground=self.WHITE,
            font=("Segoe UI", 10),
            borderwidth=0
        )
        style.configure(
            "Treeview.Heading",
            background="#E2E8F0",
            foreground=self.NAVY,
            font=("Segoe UI", 10, "bold"),
            padding=9
        )
        style.map(
            "Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", self.NAVY)]
        )
        style.configure("TCombobox", padding=7)

    def add_sample_books(self):
        samples = [
            FictionBook(1, "The Hobbit", "J.R.R. Tolkien", "Fantasy", "Adventure", 5),
            NonFictionBook(2, "Wings of Fire", "A.P.J. Abdul Kalam",
                           "Biography", "Autobiography", 5),
            ReferenceBook(3, "Oxford Dictionary", "Oxford Editors",
                          "Language", "Dictionary", 5),
            FictionBook(4, "Pride and Prejudice", "Jane Austen",
                        "Classic", "Romance", 5),
            NonFictionBook(5, "A Brief History of Time", "Stephen Hawking",
                           "Science", "Popular science", 5),
        ]
        for book in samples:
            self.library.add_book(book)

    def build_layout(self):
        # Sidebar
        sidebar = tk.Frame(self.root, bg=self.NAVY, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar, text="📚  LIBRARY", bg=self.NAVY, fg=self.WHITE,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w", padx=22, pady=(28, 4))
        tk.Label(
            sidebar, text="CATALOG MANAGEMENT", bg=self.NAVY, fg="#BFDBFE",
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=24, pady=(0, 30))

        nav_items = [
            ("Dashboard / All Books", self.show_all_books),
            ("Available Books", self.show_available_books),
            ("Add New Book", self.focus_add_form),
            ("Clear Search", self.clear_search),
        ]
        for label, command in nav_items:
            tk.Button(
                sidebar, text=label, command=command,
                bg="#1E3A8A", fg=self.WHITE, activebackground="#3B82F6",
                activeforeground=self.WHITE, relief="flat", bd=0,
                anchor="w", padx=16, pady=12,
                font=("Segoe UI", 10, "bold"), cursor="hand2"
            ).pack(fill="x", padx=12, pady=5)

        tk.Label(
            sidebar,
            text="Python • OOP • Tkinter",
            bg=self.NAVY, fg="#CBD5E1",
            font=("Segoe UI", 9)
        ).pack(side="bottom", pady=22)

        # Main content area
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(side="left", fill="both", expand=True, padx=24, pady=20)

        header = tk.Frame(main, bg=self.BG)
        header.pack(fill="x", pady=(0, 16))
        tk.Label(
            header, text="Library Catalog Dashboard",
            bg=self.BG, fg=self.NAVY, font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")
        tk.Label(
            header, text="Manage books, search the catalog, and track borrowing status.",
            bg=self.BG, fg=self.MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

        # Dashboard cards
        cards = tk.Frame(main, bg=self.BG)
        cards.pack(fill="x", pady=(0, 16))
        self.total_value = self.make_stat_card(cards, "TOTAL BOOKS", "0", "#DBEAFE")
        self.available_value = self.make_stat_card(cards, "AVAILABLE", "0", "#DCFCE7")
        self.borrowed_value = self.make_stat_card(cards, "BORROWED", "0", "#FEE2E2")

        # Main work area split
        content = tk.Frame(main, bg=self.BG)
        content.pack(fill="both", expand=True)

        left = tk.Frame(content, bg=self.WHITE, padx=12, pady=8)
        left.pack(side="left", fill="y", padx=(0, 16))
        left.configure(width=300)
        left.pack_propagate(False)

        tk.Label(
            left, text="Add a Book", bg=self.WHITE, fg=self.NAVY,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 12))

        self.id_var = tk.StringVar()
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.genre_var = tk.StringVar()
        self.type_var = tk.StringVar(value="Fiction")
        self.extra_var = tk.StringVar()
        self.stock_var = tk.StringVar(value="1")

        self.add_form_field(left, "Book ID (number)", "id", self.id_var)
        self.id_entry = self.last_entry
        self.add_form_field(left, "Title", "title", self.title_var)
        self.add_form_field(left, "Author", "author", self.author_var)
        self.add_form_field(left, "Genre", "genre", self.genre_var)
        self.add_form_field(left, "Total Quantity", "stock", self.stock_var)

        tk.Label(left, text="Book Type", bg=self.WHITE, fg=self.TEXT,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(3, 2))
        type_box = ttk.Combobox(
            left, textvariable=self.type_var,
            values=["Fiction", "Non-Fiction", "Reference"],
            state="readonly"
        )
        type_box.pack(fill="x")
        type_box.bind("<<ComboboxSelected>>", self.update_extra_label)

        self.extra_label = tk.Label(
            left, text="Subgenre", bg=self.WHITE, fg=self.TEXT,
            font=("Segoe UI", 9, "bold")
        )
        self.extra_label.pack(anchor="w", pady=(3, 2))
        self.extra_entry = ttk.Entry(left, textvariable=self.extra_var)
        self.extra_entry.pack(fill="x")

        self.make_button(left, "Add Book", self.add_book, self.BLUE).pack(fill="x", pady=(7, 3))
        self.make_button(left, "Remove Selected Book", self.remove_selected, "#B91C1C").pack(fill="x", pady=3)

        # Right side: search, table, and actions
        right = tk.Frame(content, bg=self.BG)
        right.pack(side="left", fill="both", expand=True)

        search_frame = tk.Frame(right, bg=self.WHITE, padx=12, pady=12)
        search_frame.pack(fill="x", pady=(0, 12))
        tk.Label(
            search_frame, text="Search title, author, ID, or genre:",
            bg=self.WHITE, fg=self.TEXT, font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(0, 8))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        search_entry.bind("<KeyRelease>", lambda event: self.refresh_table())
        self.make_button(search_frame, "Search", self.refresh_table, self.BLUE).pack(side="left")

        action_frame = tk.Frame(right, bg=self.BG)
        action_frame.pack(fill="x", pady=(0, 12))
        tk.Label(action_frame, text="Book ID:", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 4))
        self.borrow_id_var = tk.StringVar()
        ttk.Entry(action_frame, textvariable=self.borrow_id_var, width=8).pack(side="left", padx=(0, 8))
        tk.Label(action_frame, text="Quantity:", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 4))
        self.borrow_qty_var = tk.StringVar(value="1")
        ttk.Entry(action_frame, textvariable=self.borrow_qty_var, width=6).pack(side="left", padx=(0, 8))
        self.make_button(action_frame, "Borrow Book", self.borrow_by_id, "#15803D").pack(side="left", padx=(0, 8))
        self.make_button(action_frame, "Return Selected", self.return_selected, "#D97706").pack(side="left", padx=(0, 8))
        self.make_button(action_frame, "View Details", self.view_details, "#475569").pack(side="left")

        table_frame = tk.Frame(right, bg=self.WHITE, padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "title", "author", "type", "genre", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        headings = {
            "id": ("ID", 45),
            "title": ("Title", 170),
            "author": ("Author", 145),
            "type": ("Type", 95),
            "genre": ("Genre", 100),
            "status": ("Status", 95),
        }
        for col, (heading, width) in headings.items():
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=width, minwidth=40, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.status_var = tk.StringVar(value="Ready.")
        tk.Label(
            main, textvariable=self.status_var, bg=self.BG, fg=self.MUTED,
            font=("Segoe UI", 9), anchor="w"
        ).pack(fill="x", pady=(10, 0))

        self.update_extra_label()

    def make_stat_card(self, parent, label, value, color):
        card = tk.Frame(parent, bg=self.WHITE, padx=16, pady=12, highlightbackground="#E2E8F0", highlightthickness=1)
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))
        tk.Label(card, text=label, bg=self.WHITE, fg=self.MUTED,
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        value_label = tk.Label(card, text=value, bg=self.WHITE, fg=self.NAVY,
                               font=("Segoe UI", 22, "bold"))
        value_label.pack(anchor="w", pady=(4, 0))
        return value_label

    def add_form_field(self, parent, label, field_name, variable=None):
        tk.Label(
            parent, text=label, bg=self.WHITE, fg=self.TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", pady=(7, 4))
        if field_name == "id":
            self.last_entry = ttk.Entry(parent, textvariable=variable)
            self.last_entry.pack(fill="x")
        else:
            entry = ttk.Entry(parent, textvariable=variable)
            entry.pack(fill="x")
            self.last_entry = entry

    def make_button(self, parent, text, command, color):
        return tk.Button(
            parent, text=text, command=command, bg=color, fg=self.WHITE,
            activebackground=color, activeforeground=self.WHITE,
            relief="flat", bd=0, padx=12, pady=9,
            font=("Segoe UI", 9, "bold"), cursor="hand2"
        )

    def update_extra_label(self, event=None):
        labels = {
            "Fiction": "Subgenre",
            "Non-Fiction": "Subject",
            "Reference": "Reference Type"
        }
        self.extra_label.config(text=labels.get(self.type_var.get(), "Extra detail"))

    def add_book(self):
        try:
            book_id = int(self.id_var.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Book ID", "Please enter a numeric Book ID.")
            return

        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        genre = self.genre_var.get().strip()
        extra = self.extra_var.get().strip()
        book_type = self.type_var.get()

        try:
            total_quantity = int(self.stock_var.get().strip())
            if total_quantity < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Quantity",
                "Total quantity must be a positive whole number."
            )
            return

        if not title or not author or not genre or not extra:
            messagebox.showwarning(
                "Missing Information",
                "Please fill in the title, author, genre, and type-specific detail."
            )
            return

        if book_type == "Fiction":
            book = FictionBook(book_id, title, author, genre, extra, total_quantity)
        elif book_type == "Non-Fiction":
            book = NonFictionBook(book_id, title, author, genre, extra, total_quantity)
        else:
            book = ReferenceBook(book_id, title, author, genre, extra, total_quantity)

        success, message = self.library.add_book(book)
        if success:
            self.clear_form()
            self.refresh_table()
            self.status_var.set(message)
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Unable to Add Book", message)

    def clear_form(self):
        self.id_var.set("")
        self.title_var.set("")
        self.author_var.set("")
        self.genre_var.set("")
        self.extra_var.set("")
        self.stock_var.set("1")
        self.type_var.set("Fiction")
        self.update_extra_label()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        keyword = self.search_var.get()
        for book in self.library.search_books(keyword):
            book_type = type(book).__name__.replace("Book", "")
            status = f"{book.available_quantity}/{book.total_quantity} available"
            self.tree.insert(
                "", "end", iid=str(book.book_id),
                values=(book.book_id, book.title, book.author,
                        book_type, book.genre, status)
            )

        self.update_stats()
        self.selected_book_id = None
        self.status_var.set(
            f"Showing {len(self.tree.get_children())} book(s). "
            "Select a book to view details, return copies, or remove it."
        )

    def update_stats(self):
        borrowed = sum(book.borrowed_quantity for book in self.library.books)
        available = sum(book.available_quantity for book in self.library.books)
        total = sum(book.total_quantity for book in self.library.books)
        self.total_value.config(text=str(total))
        self.available_value.config(text=str(available))
        self.borrowed_value.config(text=str(borrowed))

    def selected_book(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book from the table first.")
            return None
        try:
            book_id = int(selection[0])
        except ValueError:
            return None
        return self.library.find_book(book_id)

    def on_select(self, event=None):
        selection = self.tree.selection()
        self.selected_book_id = int(selection[0]) if selection else None



    def borrow_by_id(self):
        try:
            book_id = int(self.borrow_id_var.get().strip())
            quantity = int(self.borrow_qty_var.get().strip())
            if quantity < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter a numeric Book ID and a positive whole-number quantity.")
            return

        success, message = self.library.borrow_book(book_id, quantity)
        if success:
            self.refresh_table()
            self.status_var.set(message)
            messagebox.showinfo("Borrow Book", message)
        else:
            self.status_var.set(message)
            messagebox.showwarning("Cannot Borrow Book", message)

    def return_selected(self):
        book = self.selected_book()
        if book is None:
            return
        try:
            quantity = int(self.borrow_qty_var.get().strip())
            if quantity < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Quantity", "Enter a positive whole-number quantity.")
            return
        success, message = self.library.return_book(book.book_id, quantity)
        if success:
            self.refresh_table()
            self.status_var.set(message)
            messagebox.showinfo("Return Book", message)
        else:
            messagebox.showwarning("Return Book", message)

    def remove_selected(self):
        book = self.selected_book()
        if book is None:
            return
        confirm = messagebox.askyesno(
            "Confirm Removal",
            f"Remove '{book.title}' from the catalog?"
        )
        if not confirm:
            return
        success, message = self.library.remove_book(book.book_id)
        if success:
            self.refresh_table()
            self.status_var.set(message)
            messagebox.showinfo("Remove Book", message)
        else:
            messagebox.showwarning("Remove Book", message)

    def view_details(self):
        book = self.selected_book()
        if book is None:
            return
        messagebox.showinfo("Book Details", book.display_details())

    def show_all_books(self):
        self.search_var.set("")
        self.refresh_table()

    def show_available_books(self):
        self.search_var.set("")
        for item in self.tree.get_children():
            self.tree.delete(item)
        available = self.library.available_books()
        for book in available:
            book_type = type(book).__name__.replace("Book", "")
            self.tree.insert(
                "", "end", iid=str(book.book_id),
                values=(book.book_id, book.title, book.author,
                        book_type, book.genre, "Available")
            )
        self.update_stats()
        self.status_var.set(f"Showing {len(available)} available book(s).")

    def focus_add_form(self):
        self.id_entry.focus_set()

    def clear_search(self):
        self.search_var.set("")
        self.refresh_table()

root = tk.Tk()
app = LibraryApp(root)
root.mainloop()
