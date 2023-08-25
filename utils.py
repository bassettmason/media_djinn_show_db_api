from google.cloud import firestore
from google.cloud.firestore import SERVER_TIMESTAMP
import os
import logging
# Logging setup

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def remove_null_values(d):
    """Recursively remove keys with null values from a dictionary."""
    if not isinstance(d, dict):
        return d
    return {k: remove_null_values(v) for k, v in d.items() if v is not None}

def initialize_firestore():
    """Initialize and return a Firestore client."""
    return firestore.Client()

def add_show_to_firestore(db, tmdb_id, show_data):
    """Add or merge a show object to Firestore."""
    shows_ref = db.collection('shows')
    show_doc_ref = shows_ref.document(tmdb_id)
    show_doc_ref.set(shows_data, merge=True)

def add_show_list_to_firestore(db, name, media_list):
    """Add a show list to Firestore."""
    show_lists_ref = db.collection('show-lists')
    show_lists_ref.document(name).set({
        'media_list': media_list,
        'date_modified': SERVER_TIMESTAMP
    })
