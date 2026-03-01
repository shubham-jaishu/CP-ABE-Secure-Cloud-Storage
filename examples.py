"""
Example usage demonstrations for CP-ABE Secure Cloud Storage System
This script shows various use cases and scenarios
"""

import requests
import json


BASE_URL = "http://localhost:8080"


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def example_1_basic_encryption():
    """Example 1: Basic file encryption with simple policy"""
    print_section("EXAMPLE 1: Basic Encryption with Simple Policy")
    
    # Create sample file
    content = b"Patient Record: John Doe, Age 45, Diagnosis: Hypertension"
    filename = "patient_record.txt"
    
    with open(filename, 'wb') as f:
        f.write(content)
    
    # Encrypt with simple policy
    policy = "Role=Doctor"
    
    print(f"📄 File: {filename}")
    print(f"🔒 Policy: {policy}")
    print(f"📊 File size: {len(content)} bytes\n")
    
    with open(filename, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/encrypt",
            files={'file': f},
            data={'policy': policy}
        )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Encryption successful!")
        print(f"   Encrypted filename: {result['encrypted_filename']}")
        print(f"   Encryption time: {result['metrics']['encryption_time']}")
        print(f"   CPU usage: {result['metrics']['cpu_percent']}%")
        return result['encrypted_filename']
    else:
        print(f"❌ Error: {response.json()}")
        return None


def example_2_and_policy():
    """Example 2: Encryption with AND policy"""
    print_section("EXAMPLE 2: Encryption with AND Policy")
    
    content = b"Confidential Research Data - Project Phoenix"
    filename = "research_data.txt"
    
    with open(filename, 'wb') as f:
        f.write(content)
    
    # AND policy - both conditions must be satisfied
    policy = "Role=Researcher AND Department=AI"
    
    print(f"📄 File: {filename}")
    print(f"🔒 Policy: {policy}")
    print(f"📝 This file requires BOTH Role=Researcher AND Department=AI\n")
    
    with open(filename, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/encrypt",
            files={'file': f},
            data={'policy': policy}
        )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Encryption successful!")
        print(f"   Encrypted filename: {result['encrypted_filename']}")
        return result['encrypted_filename']
    else:
        print(f"❌ Error: {response.json()}")
        return None


def example_3_or_policy():
    """Example 3: Encryption with OR policy"""
    print_section("EXAMPLE 3: Encryption with OR Policy")
    
    content = b"System Maintenance Log - Server Updates"
    filename = "maintenance_log.txt"
    
    with open(filename, 'wb') as f:
        f.write(content)
    
    # OR policy - either condition can be satisfied
    policy = "Role=Admin OR Role=SysOps"
    
    print(f"📄 File: {filename}")
    print(f"🔒 Policy: {policy}")
    print(f"📝 This file can be accessed by EITHER Admin OR SysOps\n")
    
    with open(filename, 'rb') as f:
        response = requests.post(
            f"{BASE_URL}/encrypt",
            files={'file': f},
            data={'policy': policy}
        )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Encryption successful!")
        print(f"   Encrypted filename: {result['encrypted_filename']}")
        return result['encrypted_filename']
    else:
        print(f"❌ Error: {response.json()}")
        return None


def example_4_successful_decryption(encrypted_filename, policy_type):
    """Example 4: Successful decryption with matching attributes"""
    print_section(f"EXAMPLE 4: Successful Decryption ({policy_type})")
    
    # Define user attributes based on policy type
    if policy_type == "simple":
        user_attrs = {"Role": "Doctor"}
    elif policy_type == "and":
        user_attrs = {"Role": "Researcher", "Department": "AI"}
    else:  # or
        user_attrs = {"Role": "Admin"}
    
    print(f"👤 User Attributes: {json.dumps(user_attrs, indent=2)}")
    print(f"📦 Encrypted File: {encrypted_filename}\n")
    
    response = requests.post(
        f"{BASE_URL}/decrypt",
        json={
            "encrypted_filename": encrypted_filename,
            "user_attributes": user_attrs
        }
    )
    
    if response.status_code == 200:
        print("✅ Access GRANTED - Decryption successful!")
        print(f"📄 Decrypted content: {response.content.decode()}")
    else:
        print(f"❌ Access DENIED: {response.json()}")


def example_5_failed_decryption(encrypted_filename):
    """Example 5: Failed decryption with wrong attributes"""
    print_section("EXAMPLE 5: Failed Decryption (Access Denied)")
    
    # Try to access research data with wrong attributes
    user_attrs = {"Role": "Intern", "Department": "HR"}
    
    print(f"👤 User Attributes: {json.dumps(user_attrs, indent=2)}")
    print(f"📦 Encrypted File: {encrypted_filename}")
    print(f"📝 These attributes do NOT satisfy the policy\n")
    
    response = requests.post(
        f"{BASE_URL}/decrypt",
        json={
            "encrypted_filename": encrypted_filename,
            "user_attributes": user_attrs
        }
    )
    
    if response.status_code == 403:
        result = response.json()
        print("❌ Access DENIED (as expected):")
        print(f"   Reason: {result['reason']}")
        print(f"   Required Policy: {result['policy']}")
    else:
        print(f"Unexpected response: {response.json()}")


def example_6_complex_scenarios():
    """Example 6: Complex real-world scenarios"""
    print_section("EXAMPLE 6: Real-World Scenarios")
    
    scenarios = [
        {
            "name": "Medical Records",
            "policy": "Role=Doctor AND Department=Cardiology",
            "content": b"ECG Report - Patient ID: 12345",
            "valid_user": {"Role": "Doctor", "Department": "Cardiology"},
            "invalid_user": {"Role": "Nurse", "Department": "Cardiology"}
        },
        {
            "name": "Financial Reports",
            "policy": "Role=CFO OR Role=Auditor",
            "content": b"Q4 2025 Financial Summary - Confidential",
            "valid_user": {"Role": "Auditor", "Level": "Senior"},
            "invalid_user": {"Role": "Manager", "Department": "Sales"}
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n--- Scenario {i}: {scenario['name']} ---\n")
        
        # Create and encrypt file
        filename = f"scenario_{i}.txt"
        with open(filename, 'wb') as f:
            f.write(scenario['content'])
        
        print(f"Policy: {scenario['policy']}")
        
        with open(filename, 'rb') as f:
            encrypt_response = requests.post(
                f"{BASE_URL}/encrypt",
                files={'file': f},
                data={'policy': scenario['policy']}
            )
        
        if encrypt_response.status_code == 200:
            encrypted_filename = encrypt_response.json()['encrypted_filename']
            
            # Test with valid user
            print(f"\n✅ Testing with valid user: {scenario['valid_user']}")
            decrypt_response = requests.post(
                f"{BASE_URL}/decrypt",
                json={
                    "encrypted_filename": encrypted_filename,
                    "user_attributes": scenario['valid_user']
                }
            )
            print(f"   Result: {'✅ Access Granted' if decrypt_response.status_code == 200 else '❌ Access Denied'}")
            
            # Test with invalid user
            print(f"\n❌ Testing with invalid user: {scenario['invalid_user']}")
            decrypt_response = requests.post(
                f"{BASE_URL}/decrypt",
                json={
                    "encrypted_filename": encrypted_filename,
                    "user_attributes": scenario['invalid_user']
                }
            )
            print(f"   Result: {'✅ Access Granted' if decrypt_response.status_code == 200 else '❌ Access Denied (Expected)'}")


def example_7_list_and_metrics():
    """Example 7: List files and view metrics"""
    print_section("EXAMPLE 7: System Information")
    
    # List all encrypted files
    print("📋 All Encrypted Files:\n")
    response = requests.get(f"{BASE_URL}/list")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Total files: {result['count']}\n")
        
        for file_info in result['files']:
            print(f"  • {file_info['original_filename']}")
            print(f"    Policy: {file_info['policy']}")
            print(f"    Encrypted as: {file_info['encrypted_filename']}\n")
    
    # Get system metrics
    print("\n📊 System Metrics:\n")
    response = requests.get(f"{BASE_URL}/metrics")
    
    if response.status_code == 200:
        result = response.json()
        metrics = result['metrics']
        print(f"  CPU Usage: {metrics['cpu_percent']}%")
        print(f"  Memory Usage: {metrics['memory_percent']}%")
        print(f"  Disk Usage: {metrics['disk_percent']}%")
        print(f"  Storage Mode: {result['storage_mode']}")


def run_all_examples():
    """Run all example demonstrations"""
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#  CP-ABE SECURE CLOUD STORAGE - COMPREHENSIVE EXAMPLES" + " "*14 + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    try:
        # Check server connection
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            raise Exception("Server not responding")
        
        print("\n✅ Connected to server at", BASE_URL)
        
        # Run examples
        encrypted_1 = example_1_basic_encryption()
        if encrypted_1:
            example_4_successful_decryption(encrypted_1, "simple")
        
        encrypted_2 = example_2_and_policy()
        if encrypted_2:
            example_4_successful_decryption(encrypted_2, "and")
            example_5_failed_decryption(encrypted_2)
        
        encrypted_3 = example_3_or_policy()
        if encrypted_3:
            example_4_successful_decryption(encrypted_3, "or")
        
        example_6_complex_scenarios()
        example_7_list_and_metrics()
        
        print_section("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to server at", BASE_URL)
        print("\nPlease start the Flask server first:")
        print("  ./start.sh")
        print("  OR")
        print("  python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    run_all_examples()
