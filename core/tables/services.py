from typing import Optional, Dict, Any
from django.db.models import QuerySet

from core.tables.models import Table


class TableService:
    """Service class for handling table-related business logic."""

    @staticmethod
    def get_available_tables() -> QuerySet[Table]:
        return Table.objects.filter(is_available=True)

    def calculate_table_price(self, table: Table, seats_requested: int) -> float:
        """Calculate the price for a table reservation."""
        # If booking the entire table, apply the discount (M-1)*X
        if seats_requested == table.seats:
            return float(table.price_per_seat * (table.seats - 1))

        # Otherwise, charge per seat (X per seat)
        return float(table.price_per_seat * seats_requested)

    def find_optimal_table(self, people_count: int) -> Optional[Dict[str, Any]]:
        """Find the optimal table for the given number of people.

        Rules:
        1. Tables have 4-10 seats
        2. Cannot book odd number of seats unless it equals table's total seats
        3. System offers the cheapest price option
        """
        available_tables = self.get_available_tables()

        if not available_tables:
            return None

        # Handle odd number of people
        adjusted_people_count = people_count
        if people_count % 2 != 0:  # If odd number
            # First try to find a table with exactly this many seats
            exact_match = available_tables.filter(seats=people_count).first()
            if exact_match:
                return {
                    "table": exact_match,
                    "seats_allocated": people_count,
                    "price": self.calculate_table_price(exact_match, people_count),
                }
            # If no exact match, round up to next even number
            adjusted_people_count = people_count + 1

        # Find tables with enough seats
        suitable_tables = available_tables.filter(seats__gte=adjusted_people_count)

        if not suitable_tables:
            return None

        # Find the cheapest option
        cheapest_option = None
        lowest_price = float("inf")

        for table in suitable_tables:
            # Calculate price based on adjusted people count
            price = self.calculate_table_price(table, adjusted_people_count)
            if price < lowest_price:
                lowest_price = price
                cheapest_option = {
                    "table": table,
                    "seats_allocated": adjusted_people_count,
                    "price": price,
                }

        return cheapest_option
