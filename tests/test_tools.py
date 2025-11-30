"""Tests for the calculator tools."""

import pytest

from mcp_starter.tools.calculator import add, divide, multiply, subtract


# Tests for the add function
def test_add_positive_numbers():
    """Test adding two positive numbers."""
    assert add(2, 3) == 5


def test_add_negative_numbers():
    """Test adding two negative numbers."""
    assert add(-2, -3) == -5


def test_add_mixed_numbers():
    """Test adding a positive and negative number."""
    assert add(-2, 3) == 1


def test_add_floats():
    """Test adding floating point numbers."""
    assert add(2.5, 3.5) == 6.0


# Tests for the subtract function
def test_subtract_positive_numbers():
    """Test subtracting two positive numbers."""
    assert subtract(5, 3) == 2


def test_subtract_negative_result():
    """Test subtraction resulting in negative number."""
    assert subtract(3, 5) == -2


def test_subtract_floats():
    """Test subtracting floating point numbers."""
    assert subtract(5.5, 2.5) == 3.0


# Tests for the multiply function
def test_multiply_positive_numbers():
    """Test multiplying two positive numbers."""
    assert multiply(2, 3) == 6


def test_multiply_with_zero():
    """Test multiplying by zero."""
    assert multiply(5, 0) == 0


def test_multiply_negative_numbers():
    """Test multiplying two negative numbers."""
    assert multiply(-2, -3) == 6


def test_multiply_floats():
    """Test multiplying floating point numbers."""
    assert multiply(2.5, 4) == 10.0


# Tests for the divide function
def test_divide_positive_numbers():
    """Test dividing two positive numbers."""
    assert divide(6, 2) == 3


def test_divide_with_remainder():
    """Test division with remainder."""
    assert divide(7, 2) == 3.5


def test_divide_by_zero():
    """Test division by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)


def test_divide_floats():
    """Test dividing floating point numbers."""
    assert divide(7.5, 2.5) == 3.0
