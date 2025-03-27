# Phorest Tech Test - Aasim

## Overview
This project is a solution to the Phorest Salon Software backend technical test. The task involves processing salon data stored in CSV files (`clients.csv`, `appointments.csv`, `services.csv`, `purchases.csv`) to identify the top 50 most loyal clients based on loyalty points earned from services and product purchases. The requirements include:

- **Data Migration**: Migrate the provided CSV data into a database of choice (SQLite used here).
- **Loyalty Calculation**: Calculate total loyalty points per client from services and purchases since January 1, 2018 (configurable), excluding banned clients.
- **Output**: Return a list of the top 50 clients (configurable) by points, including their first name, last name, email, and total points.
- **Testing**: Provide tests, even if the solution is partial, as testing is prioritized over completeness without tests.

The solution uses Python with `pandas` for CSV parsing, SQLite for data storage, and `pytest` for testing. It includes a command-line script (`run.py`) to display results and a test suite covering key components.

## Project Structure
```
phorest-techtest-Aasim/
├── data/                # Provided CSV files
│   ├── clients.csv
│   ├── appointments.csv
│   ├── services.csv
│   ├── purchases.csv
├── src/                 # Source code as a Python package
│   ├── __init__.py
│   ├── database.py     # SQLite database setup
│   ├── data_loader.py  # CSV-to-database loading
│   ├── loyalty.py      # Loyalty points calculation
├── tests/               # Test suite
│   ├── test_database.py
│   ├── test_data_loader.py
│   ├── test_loyalty.py
├── .gitignore          # Ignores venv/, *.db, __pycache__/
├── README.md           # This file
├── requirements.txt    # Dependencies
├── run.py              # Main script to run the solution
├── venv/               # Virtual environment (ignored by Git)
```

## Setup
1. **Clone the Repository** (if applicable):
   ```bash
   git clone https://github.com/Aasimshah7/phorest-techtest-Aasim.git
   cd phorest-techtest-Aasim
   ```
2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```
3. **Activate It**:
   ```bash
   venv\Scripts\activate
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   - Requires `pandas` and `pytest`.

## Running
Run the main script to see the top clients:
```bash
python run.py [top_n] [since_date]
```
- **Examples**:
  - `python run.py` - Top 50 clients since 2018-01-01 (default).
  - `python run.py 10 2020-01-01` - Top 10 clients since 2020-01-01.
- **Parameters**:
  - `top_n`: Integer for number of clients to return (default: 50).
  - `since_date`: Date in YYYY-MM-DD format (default: 2018-01-01).
- **Output**:
  - Lists clients with their first name, last name, email, and total points.
  - Returns "No clients found" if no results match the criteria (e.g., date too recent or all clients banned).

## Testing
Run the test suite:
```bash
python -m pytest tests/ -v
```
- **Tests Included**:
  - **`test_database.py`**: Verifies that `Database` creates the expected tables (`clients`, `appointments`, `services`, `purchases`).
  - **`test_data_loader.py`**: Ensures `DataLoader` populates all tables with data from CSVs.
  - **`test_loyalty.py`**: Checks that `LoyaltyAnalyzer` returns the correct top clients with required fields and non-negative points.
- **Note**: Tests use temporary `.db` files (e.g., `test_loyalty.db`), cleaned up before each run to avoid Windows file locking issues.

## Implementation Details
- **Database**:
  - SQLite is used for its simplicity and zero-configuration setup.
  - Tables match the CSV schemas:
    - `clients`: `id` (TEXT PRIMARY KEY), `first_name`, `last_name`, `email`, `phone`, `gender`, `banned` (BOOLEAN).
    - `appointments`: `id` (TEXT PRIMARY KEY), `client_id` (TEXT), `start_time`, `end_time`.
    - `services`: `id` (TEXT PRIMARY KEY), `appointment_id` (TEXT), `name`, `price` (REAL), `loyalty_points` (INTEGER).
    - `purchases`: `id` (TEXT PRIMARY KEY), `appointment_id` (TEXT), `name`, `price` (REAL), `loyalty_points` (INTEGER).
- **Data Loading**:
  - `DataLoader` uses `pandas.read_csv` to parse CSVs and `to_sql` to load data into SQLite, closing connections explicitly to prevent leaks.
- **Loyalty Calculation**:
  - `LoyaltyAnalyzer` uses a SQL query with `LEFT JOIN`s to sum loyalty points from `services` and `purchases`, filtering by `since_date` and excluding banned clients (`banned = 0`).
  - Results are sorted by total points descending and limited to `top_n`.
- **Main Script**:
  - `run.py` provides a configurable interface, accepting `top_n` and `since_date` via command-line arguments with defaults.

## Notes
- **Design Choices**:
  - SQLite chosen for ease of use; a production system might use PostgreSQL for scalability.
  - `src/` is a Python package with `__init__.py` for proper module organization and import reliability.
- **Potential Improvements**:
  - Add try-except blocks for file operations and database errors.
  - Implement logging for debugging and auditing.
  - Validate `since_date` format and range.
  - Add more tests (e.g., missing files, invalid dates, zero-point cases).