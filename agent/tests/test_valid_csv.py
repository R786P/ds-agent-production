hereimport sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.security import validate_csv_input, safe_load_csv

def test_valid_csv():
    csv = "name,age\nRahul,25\nPriya,30"
    assert validate_csv_input(csv) == True
    df = safe_load_csv(csv)
    assert len(df) == 2

def test_invalid_csv():
    bad_csv = "this is not a csv"
    assert validate_csv_input(bad_csv) == False

def test_large_csv():
    large_csv = "a,b\n" + "x,y\n" * 20000  # ~200KB, should pass
    assert validate_csv_input(large_csv, max_size_kb=500) == True

def test_code_injection():
    malicious = "name,age\nRahul,25\n__import__('os').system('rm -rf /')"
    assert validate_csv_input(malicious) == False

if __name__ == "__main__":
    test_valid_csv()
    test_invalid_csv()
    test_large_csv()
    test_code_injection()
    print("✅ All security tests passed!")
