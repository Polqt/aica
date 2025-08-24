from datetime import datetime

def parse_date_string(v):
    """Helper function to parse date strings."""
    if v is None or v == '':
        return None
    if isinstance(v, str):
        try:
            return datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Invalid date format, expected YYYY-MM-DD')
    return v