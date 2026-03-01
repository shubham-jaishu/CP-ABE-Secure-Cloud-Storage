#!/bin/bash

# Cleanup script for CP-ABE Secure Cloud Storage System

echo "================================================"
echo "CP-ABE System Cleanup Utility"
echo "================================================"
echo ""
echo "⚠️  WARNING: This will delete system data!"
echo ""
echo "What would you like to clean up?"
echo ""
echo "1) Clear all encrypted files and metadata"
echo "2) Clear logs only"
echo "3) Clear encryption key (⚠️  DANGER!)"
echo "4) Full reset (everything except source code)"
echo "5) Cancel"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        read -p "Delete all encrypted files and metadata? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            rm -rf encrypted_files/*
            rm -rf metadata/*
            echo "✅ Encrypted files and metadata cleared"
            echo "📁 Directories preserved"
        else
            echo "❌ Cancelled"
        fi
        ;;
    
    2)
        echo ""
        read -p "Delete all log files? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            rm -f cpabe_system.log
            rm -f output.log
            rm -f nohup.out
            echo "✅ Logs cleared"
        else
            echo "❌ Cancelled"
        fi
        ;;
    
    3)
        echo ""
        echo "⚠️  DANGER: Deleting the encryption key will make all"
        echo "   encrypted files permanently unrecoverable!"
        echo ""
        read -p "Are you ABSOLUTELY SURE? Type 'DELETE KEY': " confirm
        if [ "$confirm" = "DELETE KEY" ]; then
            rm -f encryption.key
            echo "✅ Encryption key deleted"
            echo "⚠️  All encrypted files are now unrecoverable!"
        else
            echo "❌ Cancelled (wise choice)"
        fi
        ;;
    
    4)
        echo ""
        echo "⚠️  This will delete:"
        echo "   - All encrypted files"
        echo "   - All metadata"
        echo "   - All logs"
        echo "   - Encryption key"
        echo "   - Test files"
        echo ""
        echo "   Source code and documentation will be preserved"
        echo ""
        read -p "Type 'FULL RESET' to confirm: " confirm
        if [ "$confirm" = "FULL RESET" ]; then
            rm -rf encrypted_files/*
            rm -rf metadata/*
            rm -f encryption.key
            rm -f cpabe_system.log
            rm -f output.log
            rm -f nohup.out
            rm -f *.txt 2>/dev/null
            rm -f scenario_*.txt 2>/dev/null
            rm -rf __pycache__
            rm -rf venv
            echo "✅ Full reset complete"
            echo ""
            echo "To start fresh:"
            echo "  python3 -m venv venv"
            echo "  source venv/bin/activate"
            echo "  pip install -r requirements.txt"
            echo "  python app.py"
        else
            echo "❌ Cancelled"
        fi
        ;;
    
    5)
        echo "❌ Cancelled"
        ;;
    
    *)
        echo "❌ Invalid choice"
        ;;
esac

echo ""
echo "Done!"
