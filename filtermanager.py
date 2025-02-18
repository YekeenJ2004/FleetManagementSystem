from constants import SQL_MAPPINGS
import logging
from typing import Dict, Any, Tuple, List
from customtypes import FromRange, ToRange, RangeField


class FilterManager:
    """
    A class to manage and apply filters for querying a database.

    This class builds SQL `WHERE` clauses based on user-provided filters and
    manages resetting the filters to their default states.
    """
    def __init__(self, filters: Dict[str, Any]) -> None:
        """
        Initialize the FilterManager with a dictionary of filters.

        Args:
            filters (Dict[str, Any]): A dictionary where keys are filter names
            and values are tkinter widgets.
        """
        self.filters = filters

    def apply_filters(self) -> Tuple[str, List[Any]]:
        """
        Build the SQL `WHERE` clause and corresponding values based on the
        filters.

        Returns:
            Tuple[str, List[Any]]: A tuple containing the SQL query string and
            the list of query parameters.
        """
        where_clauses = []
        values = []

        try:
            def add_range_filter(
                field_from: FromRange, field_to: ToRange, db_field: RangeField
            ) -> None:
                """
                Add range filters for date or year fields to the query.

                Args:
                    field_from (str): The filter name for the start of the range.
                    field_to (str): The filter name for the end of the range.
                    db_field (str): The database column name to filter.
                """
                from_widget = self.filters.get(field_from)
                to_widget = self.filters.get(field_to)

                from_value = from_widget.get() if from_widget else ""
                to_value = to_widget.get() if to_widget else ""

                if not from_value or from_value == "All":
                    from_value = None
                if not to_value or to_value == "All":
                    to_value = None

                if from_value and to_value and int(to_value.replace("-", "")) < int(from_value.replace("-", "")):
                    print("re")
                    self.handle_invalid_range(field_from, field_to)
                    logging.error(
                        f"Invalid range: {field_to} < {field_from}"
                    )
                    return
                if from_value:
                    where_clauses.append(f'"{db_field}" >= ?')
                    values.append(from_value)
                if to_value:
                    where_clauses.append(f'"{db_field}" <= ?')
                    values.append(to_value)

            # Search Bar
            search_query = self.filters.get("Search", "").get().strip()
            if search_query:
                search_fields = [
                    "Type", "RegistrationNumber", "TaxStatus", "FuelType"
                ]
                search_fields = [
                    "Type", "RegistrationNumber", "TaxStatus", "FuelType"
                ]
                search_conditions = " OR ".join(
                    [f'"{field}" LIKE ?' for field in search_fields]
                )
                where_clauses.append(f"({search_conditions})")
                values.extend([f"%{search_query}%"] * len(search_fields))

            # Range Filters
            if "Year From" in self.filters and "Year To" in self.filters:
                add_range_filter("Year From", "Year To", "ManufactureYear")
            if (
                "Tax Due Date From" in self.filters and
                "Tax Due Date To" in self.filters
            ):
                add_range_filter(
                    "Tax Due Date From",
                    "Tax Due Date To",
                    "TaxDueDate"
                )
            if (
                "Service Date From" in self.filters and
                "Service Date To" in self.filters
            ):
                add_range_filter(
                    "Service Date From", "Service Date To", "ServiceDate"
                )

        # Dropdown Filters
            for field, widget in self.filters.items():
                if field not in [
                    "Year From", "Year To", "Tax Due Date From", "Tax Due Date To",
                    "Service Date From", "Service Date To", "Search", "Order By",
                    "Order Direction", "Order By", "Order Direction"
                ]:
                    value = widget.get()
                    if value and value != "All":
                        where_clauses.append(f'"{SQL_MAPPINGS[field]}" = ?')
                        values.append(value)

            query = "SELECT * FROM Vehicles"
            if where_clauses:
                query += f" WHERE {' AND '.join(where_clauses)}"

            # Order By
            order_by_column = self.filters.get("Order By").get()
            order_direction = self.filters.get("Order Direction").get()

            if order_by_column and order_direction:
                query += (
                    f" ORDER BY \"{SQL_MAPPINGS.get(order_by_column,
                                                    order_by_column)}\" "
                )
                query += (
                    f"{order_direction}"
                )

            print(query, values)
            return query, values
        except Exception as e:
            logging.error(f"Error applying filters: {e}")
            return "", []
        
    def handle_invalid_range(self, field_from: str, field_to: str) -> None:
        """
        Handle invalid range inputs (to be implemented in subclasses).
        """
        pass

    def clear_filters(self) -> None:
        """
        Reset all filters to their default values(to be implemented in subclasses)
        """
        pass
