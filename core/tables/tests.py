from django.test import TestCase
from core.tables.models import Table
from core.tables.services import TableService


class TableModelTest(TestCase):
    def setUp(self):
        self.valid_table_data = {"table_number": 1, "seats": 6, "price_per_seat": 20.00}

    def tearDown(self):
        Table.objects.all().delete()

    def test_table_number_validators(self):
        invalid_table = Table(table_number=0, seats=4, price_per_seat=15.00)
        with self.assertRaises(Exception):
            invalid_table.full_clean()

        invalid_table = Table(table_number=11, seats=4, price_per_seat=15.00)
        with self.assertRaises(Exception):
            invalid_table.full_clean()

    def test_seats_validators(self):
        invalid_table = Table(table_number=5, seats=3, price_per_seat=15.00)
        with self.assertRaises(Exception):
            invalid_table.full_clean()

        invalid_table = Table(table_number=5, seats=11, price_per_seat=15.00)
        with self.assertRaises(Exception):
            invalid_table.full_clean()


class TableServiceTest(TestCase):
    def setUp(self):
        Table.objects.all().delete()
        self.service = TableService()
        self.table1 = Table.objects.create(
            table_number=101, seats=4, price_per_seat=10.00
        )
        self.table2 = Table.objects.create(
            table_number=102, seats=6, price_per_seat=15.00, is_available=False
        )
        self.table3 = Table.objects.create(
            table_number=103, seats=6, price_per_seat=8.00
        )

    def tearDown(self):
        Table.objects.all().delete()

    def test_get_available_tables(self):
        available = TableService.get_available_tables()
        self.assertIn(self.table1, available)
        self.assertIn(self.table3, available)
        self.assertNotIn(self.table2, available)

    def test_calculate_table_price_custom_seats(self):
        price = self.service.calculate_table_price(self.table3, 5)
        self.assertEqual(price, 40.00)  # 8.00 * 5 seats

    def test_find_optimal_table_even(self):
        result = self.service.find_optimal_table(4)
        self.assertIsNotNone(result)
        self.assertEqual(result["seats_allocated"], 4)
        self.assertEqual(result["table"].table_number, 101)

    def test_find_optimal_table_odd(self):
        result = self.service.find_optimal_table(5)
        self.assertIsNotNone(result)
        self.assertEqual(result["seats_allocated"], 6)
        self.assertEqual(result["table"].table_number, 103)

    def test_find_optimal_table_no_available(self):
        Table.objects.all().update(is_available=False)
        result = self.service.find_optimal_table(4)
        self.assertIsNone(result)

    def test_find_optimal_table_with_specific_seats(self):
        result = self.service.find_optimal_table(6)
        self.assertIsNotNone(result)
        self.assertEqual(result["seats_allocated"], 6)
        self.assertEqual(result["table"].table_number, 103)
