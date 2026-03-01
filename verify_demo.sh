#!/bin/bash

# Quick verification script - Run this before your demo!

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║        CP-ABE SYSTEM - PRE-DEMO VERIFICATION                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

PASS=0
FAIL=0

# Test 1: Check if server is running
echo "🔍 Test 1: Checking if server is running..."
if curl -s http://localhost:8080/ > /dev/null 2>&1; then
    echo "✅ Server is running at http://localhost:8080"
    ((PASS++))
else
    echo "❌ Server is NOT running"
    echo "   Run: cd /Users/avaamo/Desktop/swinnyyy && python3 app.py"
    ((FAIL++))
fi
echo ""

# Test 2: Check Python dependencies
echo "🔍 Test 2: Checking Python dependencies..."
MISSING=0
for pkg in flask cryptography boto3 psutil requests; do
    if python3 -c "import $pkg" 2>/dev/null; then
        echo "   ✅ $pkg installed"
    else
        echo "   ❌ $pkg NOT installed"
        ((MISSING++))
    fi
done

if [ $MISSING -eq 0 ]; then
    echo "✅ All dependencies installed"
    ((PASS++))
else
    echo "❌ $MISSING dependencies missing"
    echo "   Run: pip3 install -r requirements.txt"
    ((FAIL++))
fi
echo ""

# Test 3: Check if project files exist
echo "🔍 Test 3: Checking project files..."
MISSING_FILES=0
for file in app.py config.py policy_engine.py encryption.py storage.py web_interface.html; do
    if [ -f "$file" ]; then
        echo "   ✅ $file exists"
    else
        echo "   ❌ $file missing"
        ((MISSING_FILES++))
    fi
done

if [ $MISSING_FILES -eq 0 ]; then
    echo "✅ All core files present"
    ((PASS++))
else
    echo "❌ $MISSING_FILES files missing"
    ((FAIL++))
fi
echo ""

# Test 4: Try a quick API call
echo "🔍 Test 4: Testing API endpoint..."
if curl -s http://localhost:8080/ | grep -q "running"; then
    echo "✅ API responding correctly"
    ((PASS++))
else
    echo "❌ API not responding properly"
    ((FAIL++))
fi
echo ""

# Test 5: Check if demo files are ready
echo "🔍 Test 5: Checking demo documentation..."
DEMO_DOCS=0
for doc in DEMO_GUIDE.md DEMO_CHEATSHEET.txt GET_STARTED.md README.md; do
    if [ -f "$doc" ]; then
        ((DEMO_DOCS++))
    fi
done

if [ $DEMO_DOCS -ge 3 ]; then
    echo "✅ Demo documentation available ($DEMO_DOCS files)"
    ((PASS++))
else
    echo "⚠️  Some demo docs missing"
    ((FAIL++))
fi
echo ""

# Final Summary
echo "═══════════════════════════════════════════════════════════════"
echo "                    VERIFICATION SUMMARY"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Tests Passed: $PASS ✅"
echo "Tests Failed: $FAIL ❌"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 ALL CHECKS PASSED - READY FOR DEMO!"
    echo ""
    echo "Quick Start Commands:"
    echo "  1. Demo guide:  cat DEMO_CHEATSHEET.txt"
    echo "  2. Health check: curl http://localhost:8080/"
    echo "  3. Run tests:    python3 test_system.py"
    echo "  4. Web UI:       open web_interface.html"
    echo ""
    echo "You're all set! 🚀"
else
    echo "⚠️  SOME CHECKS FAILED - FIX ISSUES BEFORE DEMO"
    echo ""
    echo "Common fixes:"
    echo "  • Start server: python3 app.py"
    echo "  • Install deps: pip3 install -r requirements.txt"
    echo "  • Check logs:   cat cpabe_system.log"
fi

echo "═══════════════════════════════════════════════════════════════"
