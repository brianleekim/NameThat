#!/usr/bin/env python3
"""
Test script to test API session functionality
"""
import requests

def test_api_session():
    print("Testing API session functionality...")
    
    # Create a session object to maintain cookies
    session = requests.Session()
    
    # Test the debug session endpoint
    print("Testing debug_session endpoint...")
    response = session.get('http://localhost:8000/api/debug_session/')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Cookies: {dict(session.cookies)}")
    
    # Test the test_session endpoint
    print("\nTesting test_session endpoint...")
    response = session.get('http://localhost:8000/api/test_session/')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Cookies: {dict(session.cookies)}")
    
    # Test the playlists endpoint (should fail without auth)
    print("\nTesting playlists endpoint (should fail without auth)...")
    response = session.get('http://localhost:8000/api/playlists/')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Cookies: {dict(session.cookies)}")

if __name__ == '__main__':
    test_api_session() 