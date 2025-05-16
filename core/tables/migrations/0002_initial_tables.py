from django.db import migrations


def create_initial_tables(apps, schema_editor):
    Table = apps.get_model("tables", "Table")

    # Create 10 tables with varying seat capacities
    tables_data = [
        {"table_number": 1, "seats": 4, "price_per_seat": 10.00},
        {"table_number": 2, "seats": 4, "price_per_seat": 10.00},
        {"table_number": 3, "seats": 5, "price_per_seat": 12.00},
        {"table_number": 4, "seats": 6, "price_per_seat": 12.00},
        {"table_number": 5, "seats": 7, "price_per_seat": 12.00},
        {"table_number": 6, "seats": 8, "price_per_seat": 15.00},
        {"table_number": 7, "seats": 8, "price_per_seat": 15.00},
        {"table_number": 8, "seats": 8, "price_per_seat": 15.00},
        {"table_number": 9, "seats": 9, "price_per_seat": 18.00},
        {"table_number": 10, "seats": 10, "price_per_seat": 18.00},
    ]

    for table_data in tables_data:
        Table.objects.create(
            table_number=table_data["table_number"],
            seats=table_data["seats"],
            price_per_seat=table_data["price_per_seat"],
            is_available=True,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("tables", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_initial_tables),
    ]
