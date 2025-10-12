#!/usr/bin/env python3
"""
Quick validation script to check that all exercise files are present and valid
"""

import os
import sys

TUTORIAL_DIR = os.path.dirname(os.path.abspath(__file__))

# Expected files
EXPECTED_FILES = [
    "README.md",
    "INSTRUCTOR_GUIDE.md",
    "step-1-hello-world.py",
    "step-2-json-response.py",
    "step-3-multiple-routes.py",
    "step-4-url-parameters.py",
    "step-5-query-parameters.py",
    "step-6-post-request.py",
    "step-7-validation.py",
    "step-8-full-crud.py"
]

def check_files():
    """Check if all expected files exist"""
    print("🔍 Checking tutorial files...\n")
    
    all_present = True
    for filename in EXPECTED_FILES:
        filepath = os.path.join(TUTORIAL_DIR, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✅ {filename:35} ({size:,} bytes)")
        else:
            print(f"❌ {filename:35} MISSING")
            all_present = False
    
    print()
    
    if all_present:
        print("🎉 All tutorial files are present!")
        return True
    else:
        print("⚠️  Some files are missing.")
        return False


def check_python_syntax():
    """Check if Python files have valid syntax"""
    print("\n🐍 Checking Python syntax...\n")
    
    python_files = [f for f in EXPECTED_FILES if f.endswith('.py')]
    all_valid = True
    
    for filename in python_files:
        filepath = os.path.join(TUTORIAL_DIR, filename)
        try:
            with open(filepath, 'r') as f:
                compile(f.read(), filename, 'exec')
            print(f"✅ {filename:35} Valid syntax")
        except SyntaxError as e:
            print(f"❌ {filename:35} Syntax error: {e}")
            all_valid = False
    
    print()
    
    if all_valid:
        print("🎉 All Python files have valid syntax!")
        return True
    else:
        print("⚠️  Some Python files have syntax errors.")
        return False


def main():
    print("=" * 60)
    print("Tutorial Exercise Validator")
    print("=" * 60)
    print()
    
    files_ok = check_files()
    syntax_ok = check_python_syntax()
    
    print("=" * 60)
    if files_ok and syntax_ok:
        print("✅ All checks passed! Tutorial is ready to use.")
        print()
        print("To start teaching:")
        print("  1. Open week-2/tutorial/README.md")
        print("  2. Review week-2/tutorial/INSTRUCTOR_GUIDE.md")
        print("  3. Run: ./auto/run python week-2/tutorial/step-1-hello-world.py")
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

