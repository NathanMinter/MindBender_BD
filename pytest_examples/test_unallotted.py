import ipo

def test_case_1():
    assert ipo.getUnallottedUsers([[1,5,5,0], [2,7,8,1], [3,7,5,1], [4,10,3,3]], 18) == [4]

def test_case_2():
    assert ipo.getUnallottedUsers([[1,5,5,0], [2,7,8,1]], 5) == [1]

def test_case_3():
    assert ipo.getUnallottedUsers([[1,5,5,0], [2,7,8,1], [3,7,5,1], [4,10,3,3]], 1) == [1,3,4]
