#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║           CP-ABE SYSTEM - LIVE DEMO SCRIPT                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Clean up old demo files
rm -f demo_file.txt encrypted_demo_file.txt decrypted.txt

echo "🎬 DEMO START"
echo "═════════════════════════════════════════════════════════════════"
echo ""

# Step 1: Create a demo file
echo "📝 Step 1: Creating a confidential file..."
echo "TOP SECRET: Financial Report Q4 2025 - Authorized Personnel Only" > demo_file.txt
echo "✅ File created: demo_file.txt"
echo ""
read -p "Press ENTER to continue..."
echo ""

# Step 2: Encrypt with policy
echo "🔒 Step 2: Encrypting file with policy..."
echo "Policy: Role=Manager AND Department=Finance"
echo ""
curl -X POST http://localhost:8080/encrypt \
  -F "file=@demo_file.txt" \
  -F "policy=Role=Manager AND Department=Finance" | python3 -m json.tool
echo ""
read -p "Press ENTER to continue..."
echo ""

# Step 3: Try with WRONG credentials (will fail)
echo "❌ Step 3: Trying to decrypt as 'Role=Intern'..."
echo "Expected: ACCESS DENIED"
echo ""
curl -X POST http://localhost:8080/decrypt \
  -H "Content-Type: application/json" \
  -d '{"encrypted_filename": "encrypted_demo_file.txt", "user_attributes": {"Role": "Intern", "Department": "Finance"}}' | python3 -m json.tool
echo ""
read -p "Press ENTER to continue..."
echo ""

# Step 4: Try with CORRECT credentials (will succeed)
echo "✅ Step 4: Trying to decrypt as 'Role=Manager, Department=Finance'..."
echo "Expected: ACCESS GRANTED"
echo ""
curl -X POST http://localhost:8080/decrypt \
  -H "Content-Type: application/json" \
  -d '{"encrypted_filename": "encrypted_demo_file.txt", "user_attributes": {"Role": "Manager", "Department": "Finance"}}' \
  --output decrypted.txt

if [ -f decrypted.txt ]; then
    echo ""
    echo "🎉 SUCCESS! File decrypted. Content:"
    echo "─────────────────────────────────────────────────────────────"
    cat decrypted.txt
    echo ""
    echo "─────────────────────────────────────────────────────────────"
else
    echo "❌ Decryption failed"
fi

echo ""
echo "═════════════════════════════════════════════════════════════════"
echo "🎉 DEMO COMPLETE!"
echo "═════════════════════════════════════════════════════════════════"
