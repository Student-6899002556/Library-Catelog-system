# Library Catalog System

A desktop library catalog application built with Python and Tkinter. It lets you manage books and track how many copies are available or borrowed.

## Features

- View the full catalog and filter it to books with available copies.
- Search by book title, author, ID, or genre.
- Add and remove books, with separate details for fiction, non-fiction, and reference books.
- Borrow and return multiple copies while preventing unavailable quantities from being borrowed or returned.
- View book details and catalog-wide copy counts.
- Start with a small set of sample books.

## Requirements

- Python 3 with Tkinter available.

Tkinter is included with many Python installations. On some Linux distributions it is provided by a separate system package.

## Run

From the project directory, run:

```bash
python minproj.py
```

On Windows, you can also use:

```powershell
py minproj.py
```

The application opens a desktop window. Use the book ID and quantity fields to borrow copies. To return copies, switch to **Dashboard / All Books** if needed, select the book, and use **Return Selected**.

## Data storage

Books are stored in memory while the application is open. The sample books are re-created each time it starts, and changes made during a session are not saved after closing the application.

## Project structure

- `minproj.py` — book models, catalog operations, and the Tkinter user interface.
