from utils import remove_null_values, initialize_firestore, add_show_to_firestore, add_show_list_to_firestore

# Initializing Firestore client
db = initialize_firestore()

def show_db(request):
    """Adds a show object or a show list to the Firestore database."""
    if request.method != 'POST':
        return 'Only POST requests are allowed', 405

    request_json = request.get_json(silent=True)
    
    # Check for show list POST request
    if 'name' in request_json and 'media_list' in request_json:
        return process_show_list(request_json)
    # Otherwise, assume it's a show POST request
    elif 'title' in request_json and 'ids' in request_json:
        return process_show(request_json)
    else:
        return 'Invalid POST request format', 400

def process_show(show_data):
    """Process a single show object."""
    if not all(key in show_data for key in ['title', 'year', 'ids']):
        return 'Invalid show object provided', 400

    tmdb_id = show_data['ids'].get('tmdb')
    if not tmdb_id:
        return 'No tmdb ID provided in show object', 400

    cleaned_data = remove_null_values(show_data)
    # Add show to Firestore
    add_show_to_firestore(db, tmdb_id, cleaned_data)
    
    return f'Show {tmdb_id} added successfully!', 200

def process_show_list(show_list_data):
    """Process a show list object."""
    name = show_list_data.get('name')
    media_list = show_list_data.get('media_list')

    if not name or not media_list:
        return 'Invalid show list provided', 400
    
    # Add show list to Firestore
    add_show_list_to_firestore(db, name, media_list)
    return f"show list '{name}' added successfully!", 200
