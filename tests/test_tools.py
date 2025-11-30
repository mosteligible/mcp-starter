"""Tests for the calculator tools."""

import pytest

from mcp_starter.tools.calculator import add, divide, multiply, subtract


class TestAdd:
    """Tests for the add function."""

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert add(2, 3) == 5

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert add(-2, -3) == -5

    def test_add_mixed_numbers(self):
        """Test adding a positive and negative number."""
        assert add(-2, 3) == 1

    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert add(2.5, 3.5) == 6.0


class TestSubtract:
    """Tests for the subtract function."""

    def test_subtract_positive_numbers(self):
        """Test subtracting two positive numbers."""
        assert subtract(5, 3) == 2

    def test_subtract_negative_result(self):
        """Test subtraction resulting in negative number."""
        assert subtract(3, 5) == -2

    def test_subtract_floats(self):
        """Test subtracting floating point numbers."""
        assert subtract(5.5, 2.5) == 3.0


class TestMultiply:
    """Tests for the multiply function."""

    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert multiply(2, 3) == 6

    def test_multiply_with_zero(self):
        """Test multiplying by zero."""
        assert multiply(5, 0) == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying two negative numbers."""
        assert multiply(-2, -3) == 6

    def test_multiply_floats(self):
        """Test multiplying floating point numbers."""
        assert multiply(2.5, 4) == 10.0


class TestDivide:
    """Tests for the divide function."""

    def test_divide_positive_numbers(self):
        """Test dividing two positive numbers."""
        assert divide(6, 2) == 3

    def test_divide_with_remainder(self):
        """Test division with remainder."""
        assert divide(7, 2) == 3.5

    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)

    def test_divide_floats(self):
        """Test dividing floating point numbers."""
        assert divide(7.5, 2.5) == 3.0
