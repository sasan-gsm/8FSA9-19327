from decimal import Decimal
from django.test import TestCase
from core.tables.models import Table
from core.tables.services import TableService


class TableModelTests(TestCase):
    """Tests for the Table model."""

    def setUp(self):
        self.table_data = {
            "table_number": 1,
            "seats": 6,
            "price_per_seat": Decimal("10.00"),
            "is_available": True,
        }
        self.table = Table.objects.create(**self.table_data)

    def test_table_creation(self):
        """Test creating a table is successful."""
        self.assertEqual(self.table.table_number, self.table_data["table_number"])
        self.assertEqual(self.table.seats, self.table_data["seats"])
        self.assertEqual(self.table.price_per_seat, self.table_data["price_per_seat"])
        self.assertTrue(self.table.is_available)

    def test_table_string_representation(self):
        """Test the string representation of a table."""
        expected_str = f"Table {self.table.table_number} ({self.table.seats} seats)"
        self.assertEqual(str(self.table), expected_str)


class TableServiceTests(TestCase):
    """Tests for the TableService class."""

    def setUp(self):
        self.service = TableService()
        # Create test tables
        self.table1 = Table.objects.create(
            table_number=1, seats=4, price_per_seat=Decimal("10.00")
        )
        self.table2 = Table.objects.create(
            table_number=2, seats=6, price_per_seat=Decimal("12.00")
        )
        self.table3 = Table.objects.create(
            table_number=3, seats=8, price_per_seat=Decimal("15.00")
        )

    def test_get_available_tables(self):
        """Test getting available tables."""
        available_tables = self.service.get_available_tables()
        self.assertEqual(available_tables.count(), 3)

        # Make one table unavailable
        self.table1.is_available = False
        self.table1.save()

        available_tables = self.service.get_available_tables()
        self.assertEqual(available_tables.count(), 2)

    def test_calculate_table_price(self):
        """Test calculating table price."""
        # Test partial booking
        price = self.service.calculate_table_price(self.table1, 2)
        self.assertEqual(price, 20.0)  # 2 seats * 10.00

        # Test full booking (with discount)
        price = self.service.calculate_table_price(self.table1, 4)
        self.assertEqual(price, 30.0)  # 3 seats * 10.00 (discount applied)

    def test_find_optimal_table_even_number(self):
        """Test finding optimal table for even number of people."""
        result = self.service.find_optimal_table(4)
        self.assertIsNotNone(result)
        self.assertEqual(result["table"], self.table1)
        self.assertEqual(result["seats_allocated"], 4)
        self.assertEqual(result["price"], 30.0)

    def test_find_optimal_table_odd_number(self):
        """Test finding optimal table for odd number of people."""
        # Should round up to next even number unless exact match exists
        result = self.service.find_optimal_table(5)
        self.assertIsNotNone(result)
        self.assertEqual(result["seats_allocated"], 6)

    def test_find_optimal_table_no_available(self):
        """Test finding optimal table when none are available."""
        # Make all tables unavailable
        Table.objects.all().update(is_available=False)
        result = self.service.find_optimal_table(4)
        self.assertIsNone(result)

    def test_find_optimal_table_exact_match(self):
        """Test finding optimal table with exact seat match."""
        result = self.service.find_optimal_table(6)
        self.assertIsNotNone(result)
        self.assertEqual(result["table"], self.table2)
        self.assertEqual(result["seats_allocated"], 6)
