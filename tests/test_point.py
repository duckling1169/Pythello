import pytest
import math
from game.point import Point


class TestPoint:
    """Test cases for the Point class."""

    def test_point_initialization(self):
        """Test point initialization."""
        point = Point(3, 4)
        assert point.x == 3
        assert point.y == 4

    def test_point_shift(self):
        """Test point shifting."""
        point = Point(3, 4)
        point.shift(2, -1)
        assert point.x == 5
        assert point.y == 3

    def test_point_distance(self):
        """Test distance calculation."""
        distance = Point.dist(0, 0, 3, 4)
        expected = round(math.dist([0, 0], [3, 4]), 2)
        assert distance == expected
        assert distance == 5.0

    def test_point_copy(self):
        """Test point copying."""
        original = Point(3, 4)
        copy = original.__copy__()
        
        assert copy.x == original.x
        assert copy.y == original.y
        assert copy is not original

    def test_point_equality(self):
        """Test point equality."""
        point1 = Point(3, 4)
        point2 = Point(3, 4)
        point3 = Point(3, 5)
        
        assert point1 == point2
        assert point1 != point3
        assert point1 != "not a point"

    def test_point_hash(self):
        """Test point hashing."""
        point1 = Point(3, 4)
        point2 = Point(3, 4)
        point3 = Point(3, 5)
        
        # Equal points should have same hash
        assert hash(point1) == hash(point2)
        
        # Different points should generally have different hashes
        assert hash(point1) != hash(point3)
        
        # Points should be usable in sets/dicts
        point_set = {point1, point2, point3}
        assert len(point_set) == 2  # point1 and point2 are the same

    def test_point_string_representation(self):
        """Test point string output."""
        point = Point(0, 0)
        assert str(point) == "(a, 1)"
        
        point = Point(3, 4)
        assert str(point) == "(d, 5)"
        
        point = Point(7, 7)
        assert str(point) == "(h, 8)"