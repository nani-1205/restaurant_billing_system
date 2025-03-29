from database.database_manager import get_table_status, update_table_status, create_tables_db
import logging

logging.basicConfig(level=logging.INFO)

def get_table_status(table_id):
    """Retrieves the status of a table."""
    try:
        return get_table_status(table_id)  # Call the database function
    except Exception as e:
        logging.error(f"Error getting table status for table {table_id}: {e}")
        return None

def update_table_status(table_id, status):
    """Updates the status of a table."""
    try:
        update_table_status(table_id, status) # Call the database function
    except Exception as e:
        logging.error(f"Error updating table {table_id} to status {status}: {e}")

def create_tables(num_tables):
    try:
        create_tables_db(num_tables)
    except Exception as e:
        logging.error(f"Error creating tables: {e}")