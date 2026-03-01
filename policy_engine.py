"""
Policy Engine for Attribute-Based Access Control
Supports AND/OR operations for policy evaluation
"""

import re


class PolicyEngine:
    """Evaluates access policies against user attributes"""
    
    @staticmethod
    def parse_condition(condition, user_attributes):
        """
        Parse and evaluate a single condition (e.g., "Role=Doctor")
        
        Args:
            condition (str): Single condition string
            user_attributes (dict): User's attributes
            
        Returns:
            bool: True if condition is satisfied
        """
        condition = condition.strip()
        
        # Parse attribute=value format
        if '=' in condition:
            attr, value = condition.split('=', 1)
            attr = attr.strip()
            value = value.strip()
            
            # Check if user has this attribute with matching value
            return user_attributes.get(attr) == value
        
        return False
    
    @staticmethod
    def evaluate_policy(policy_string, user_attributes):
        """
        Evaluate a policy string against user attributes
        Supports AND/OR operators
        
        Args:
            policy_string (str): Policy in format "Role=Doctor AND Department=CSE"
            user_attributes (dict): User's attributes {"Role": "Doctor", ...}
            
        Returns:
            bool: True if user satisfies the policy
        """
        if not policy_string or not user_attributes:
            return False
        
        # First, handle OR operations (lower precedence)
        if ' OR ' in policy_string:
            or_parts = policy_string.split(' OR ')
            # If any OR condition is true, return True
            for or_part in or_parts:
                if PolicyEngine.evaluate_policy(or_part.strip(), user_attributes):
                    return True
            return False
        
        # Then, handle AND operations (higher precedence)
        if ' AND ' in policy_string:
            and_parts = policy_string.split(' AND ')
            # All AND conditions must be true
            for and_part in and_parts:
                if not PolicyEngine.evaluate_policy(and_part.strip(), user_attributes):
                    return False
            return True
        
        # Base case: single condition
        return PolicyEngine.parse_condition(policy_string, user_attributes)
    
    @staticmethod
    def check_policy(policy_string, user_attributes):
        """
        Main entry point for policy checking
        
        Args:
            policy_string (str): Access policy
            user_attributes (dict): User's attributes
            
        Returns:
            tuple: (bool: access_granted, str: message)
        """
        try:
            access_granted = PolicyEngine.evaluate_policy(policy_string, user_attributes)
            
            if access_granted:
                return True, "Access granted"
            else:
                return False, "Access denied: Attributes do not satisfy policy"
                
        except Exception as e:
            return False, f"Policy evaluation error: {str(e)}"


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    engine = PolicyEngine()
    
    # Test 1: Simple AND policy
    policy1 = "Role=Doctor AND Department=CSE"
    attrs1 = {"Role": "Doctor", "Department": "CSE"}
    result1, msg1 = engine.check_policy(policy1, attrs1)
    print(f"Test 1: {result1} - {msg1}")
    
    # Test 2: OR policy
    policy2 = "Role=Doctor OR Role=Admin"
    attrs2 = {"Role": "Admin"}
    result2, msg2 = engine.check_policy(policy2, attrs2)
    print(f"Test 2: {result2} - {msg2}")
    
    # Test 3: Failed policy
    policy3 = "Role=Doctor AND Department=CSE"
    attrs3 = {"Role": "Nurse", "Department": "CSE"}
    result3, msg3 = engine.check_policy(policy3, attrs3)
    print(f"Test 3: {result3} - {msg3}")
