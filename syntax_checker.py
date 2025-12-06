"""Simple Python syntax checker"""
import os
import py_compile
import sys

def check_syntax(directory):
    """Check syntax of all Python files in directory"""
    errors = []
    files_checked = 0
    
    for root, dirs, files in os.walk(directory):
        # Skip __pycache__ and .venv
        if '__pycache__' in root or '.venv' in root or '.git' in root:
            continue
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    py_compile.compile(filepath, doraise=True)
                    print(f"✓ {filepath}")
                    files_checked += 1
                except py_compile.PyCompileError as e:
                    print(f"✗ {filepath} - SYNTAX ERROR")
                    errors.append((filepath, str(e)))
    
    print(f"\n{'='*60}")
    print(f"Files checked: {files_checked}")
    
    if errors:
        print(f"ERRORS FOUND: {len(errors)}")
        for filepath, error in errors:
            print(f"\n{filepath}:")
            print(error)
        return False
    else:
        print("✓ All Python files have valid syntax!")
        return True

if __name__ == "__main__":
    success = check_syntax("app")
    if not success:
        sys.exit(1)
