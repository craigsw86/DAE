#!/usr/bin/env python3
"""
Test Checklist Creation with Fresh Token
"""

import requests
import json

def test_checklist_creation():
    """Test checklist creation with proper authentication"""
    
    base_url = "http://localhost:8000"
    
    # Step 1: Get fresh token
    print("🔑 Getting fresh authentication token...")
    auth_data = {"username": "testuser", "password": "testpass123"}
    
    try:
        auth_response = requests.post(f"{base_url}/api/token/", json=auth_data, timeout=10)
        if auth_response.status_code == 200:
            token_data = auth_response.json()
            access_token = token_data.get('access')
            print(f"✅ Token received: {access_token[:50]}...")
            
            # Step 2: Test checklist creation
            print("\n📝 Testing checklist creation...")
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # First, let's check what regulations exist
            print("📋 Checking available regulations...")
            regs_response = requests.get(f"{base_url}/api/regulations/", headers=headers, timeout=10)
            print(f"Regulations API Status: {regs_response.status_code}")
            if regs_response.status_code == 200:
                regulations = regs_response.json()
                print(f"Available regulations: {len(regulations)}")
                for reg in regulations:
                    print(f"  - ID: {reg.get('id')}, Title: {reg.get('title')}")
            
            # Test checklist creation with different data
            test_cases = [
                {
                    "name": "Basic Creation",
                    "data": {
                        "regulation_update": 1,
                        "completed": False,
                        "notes": "Test notes",
                        "likelihood": 3,
                        "impact": 4,
                        "mitigation_steps": "Test mitigation steps"
                    }
                },
                {
                    "name": "Minimal Creation",
                    "data": {
                        "regulation_update": 1,
                        "completed": False,
                        "likelihood": 1,
                        "impact": 1
                    }
                },
                {
                    "name": "Complete Creation",
                    "data": {
                        "regulation_update": 1,
                        "completed": True,
                        "notes": "Complete test notes",
                        "admin_notes": "Admin test notes",
                        "likelihood": 5,
                        "impact": 5,
                        "mitigation_steps": "Complete mitigation steps"
                    }
                }
            ]
            
            for test_case in test_cases:
                print(f"\n🧪 Testing: {test_case['name']}")
                print(f"Data: {json.dumps(test_case['data'], indent=2)}")
                
                try:
                    create_response = requests.post(
                        f"{base_url}/api/checklist/",
                        json=test_case['data'],
                        headers=headers,
                        timeout=10
                    )
                    
                    print(f"Status: {create_response.status_code}")
                    print(f"Response: {create_response.text}")
                    
                    if create_response.status_code == 201:
                        print("✅ SUCCESS!")
                        created_item = create_response.json()
                        print(f"Created item ID: {created_item.get('id')}")
                        break
                    else:
                        print("❌ FAILED")
                        
                except Exception as e:
                    print(f"❌ ERROR: {e}")
            
        else:
            print(f"❌ Authentication failed: {auth_response.status_code}")
            print(f"Response: {auth_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_checklist_creation()
