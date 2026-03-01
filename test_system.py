"""
Test script for CP-ABE Secure Cloud Storage System
Run this after starting the Flask app to verify functionality
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:8080"


def test_health_check():
    """Test 1: Health check endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Health check failed"
    print("✅ Health check passed")


def test_encrypt_file():
    """Test 2: Encrypt a file with policy"""
    print("\n" + "="*60)
    print("TEST 2: File Encryption")
    print("="*60)
    
    # Create a test file
    test_content = b"This is sensitive medical data that needs protection."
    test_filename = "test_medical_record.txt"
    
    with open(test_filename, 'wb') as f:
        f.write(test_content)
    
    # Encrypt with policy
    policy = "Role=Doctor AND Department=CSE"
    
    with open(test_filename, 'rb') as f:
        files = {'file': f}
        data = {'policy': policy}
        response = requests.post(f"{BASE_URL}/encrypt", files=files, data=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Encryption failed"
    result = response.json()
    assert result['success'] == True, "Encryption not successful"
    
    # Clean up test file
    os.remove(test_filename)
    
    print("✅ Encryption passed")
    return result['encrypted_filename']


def test_decrypt_with_valid_attributes(encrypted_filename):
    """Test 3: Decrypt with valid attributes (should succeed)"""
    print("\n" + "="*60)
    print("TEST 3: Decryption with Valid Attributes")
    print("="*60)
    
    data = {
        "encrypted_filename": encrypted_filename,
        "user_attributes": {
            "Role": "Doctor",
            "Department": "CSE"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/decrypt",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print(f"Decrypted content: {response.content.decode()}")
        assert b"sensitive medical data" in response.content, "Decrypted content mismatch"
        print("✅ Decryption with valid attributes passed")
    else:
        print(f"Error: {response.json()}")
        raise AssertionError("Decryption should have succeeded")


def test_decrypt_with_invalid_attributes(encrypted_filename):
    """Test 4: Decrypt with invalid attributes (should fail)"""
    print("\n" + "="*60)
    print("TEST 4: Decryption with Invalid Attributes (Access Denied)")
    print("="*60)
    
    data = {
        "encrypted_filename": encrypted_filename,
        "user_attributes": {
            "Role": "Nurse",
            "Department": "CSE"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/decrypt",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 403, "Should return 403 Forbidden"
    result = response.json()
    assert result['success'] == False, "Should deny access"
    print("✅ Access denial test passed")


def test_or_policy():
    """Test 5: Test OR policy"""
    print("\n" + "="*60)
    print("TEST 5: OR Policy Test")
    print("="*60)
    
    # Create test file
    test_content = b"OR policy test data"
    test_filename = "test_or_policy.txt"
    
    with open(test_filename, 'wb') as f:
        f.write(test_content)
    
    # Encrypt with OR policy
    policy = "Role=Doctor OR Role=Admin"
    
    with open(test_filename, 'rb') as f:
        files = {'file': f}
        data = {'policy': policy}
        response = requests.post(f"{BASE_URL}/encrypt", files=files, data=data)
    
    encrypted_filename = response.json()['encrypted_filename']
    
    # Test with Admin role (should succeed)
    data = {
        "encrypted_filename": encrypted_filename,
        "user_attributes": {
            "Role": "Admin",
            "Department": "IT"
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/decrypt",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    assert response.status_code == 200, "OR policy should allow Admin"
    
    # Clean up
    os.remove(test_filename)
    
    print("✅ OR policy test passed")


def test_list_files():
    """Test 6: List all encrypted files"""
    print("\n" + "="*60)
    print("TEST 6: List Encrypted Files")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/list")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "List files failed"
    print("✅ List files test passed")


def test_metrics():
    """Test 7: Get system metrics"""
    print("\n" + "="*60)
    print("TEST 7: System Metrics")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/metrics")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Metrics endpoint failed"
    print("✅ Metrics test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*60)
    print("# CP-ABE SECURE CLOUD STORAGE - TEST SUITE")
    print("#"*60)
    
    try:
        # Test 1: Health check
        test_health_check()
        time.sleep(1)
        
        # Test 2: Encrypt file
        encrypted_filename = test_encrypt_file()
        time.sleep(1)
        
        # Test 3: Valid decryption
        test_decrypt_with_valid_attributes(encrypted_filename)
        time.sleep(1)
        
        # Test 4: Invalid decryption
        test_decrypt_with_invalid_attributes(encrypted_filename)
        time.sleep(1)
        
        # Test 5: OR policy
        test_or_policy()
        time.sleep(1)
        
        # Test 6: List files
        test_list_files()
        time.sleep(1)
        
        # Test 7: Metrics
        test_metrics()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server")
        print("Make sure the Flask app is running:")
        print("  python app.py")
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
