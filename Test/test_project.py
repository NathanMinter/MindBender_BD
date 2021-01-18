from calculator import Calculator

## Arrange
calculator = Calculator()

def test_addition():
    ## Act
    result = calculator.add(1,1)
    ## Assert
    assert result == 2

def test_multiplication():
    result = calculator.product(3,5,9)
    assert result == 135
