#!/usr/bin/env python3
"""
Test script to check if Django sessions are working properly
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jukeguesser.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

def test_session():
    print("Testing Django session functionality...")
    
    # Create a test session
    session = SessionStore()
    session['test_key'] = 'test_value'
    session.save()
    
    print(f"Created session with key: {session.session_key}")
    print(f"Session data: {dict(session)}")
    
    # Retrieve the session
    retrieved_session = SessionStore(session_key=session.session_key)
    print(f"Retrieved session data: {dict(retrieved_session)}")
    
    # Clean up
    session.delete()
    print("Session test completed successfully!")

if __name__ == '__main__':
    test_session() 