import perfectSubstring

def test_case_1():
    assert perfectSubstring.PerfectSubstring("1102021222", 2) == 6

def test_case_2():
    assert perfectSubstring.PerfectSubstring("0123456789", 4) == 0

def test_case_3():
    assert perfectSubstring.PerfectSubstring("123123", 1) == 15
