from typing import Dict, Optional, List


class UnitConverter:
    """Convert between different measurement units"""

    def __init__(self):
        self.conversion_table = self._load_conversion_table()
        self.standard_units = {
            'volume': 'ml',
            'weight': 'g',
            'temperature': 'celsius'
        }

    def _load_conversion_table(self) -> Dict:
        """Load unit conversion table"""
        return {
            'volume': {
                # All conversions to milliliters (ml)
                'ml': 1.0,
                'milliliter': 1.0,
                'milliliters': 1.0,
                'l': 1000.0,
                'liter': 1000.0,
                'liters': 1000.0,
                'cup': 236.588,
                'cups': 236.588,
                'tbsp': 14.787,
                'tablespoon': 14.787,
                'tablespoons': 14.787,
                'tsp': 4.929,
                'teaspoon': 4.929,
                'teaspoons': 4.929,
                'fl oz': 29.574,
                'fluid ounce': 29.574,
                'fluid ounces': 29.574,
                'pint': 473.176,
                'pints': 473.176,
                'quart': 946.353,
                'quarts': 946.353,
                'gallon': 3785.41,
                'gallons': 3785.41,
            },
            'weight': {
                # All conversions to grams (g)
                'g': 1.0,
                'gram': 1.0,
                'grams': 1.0,
                'kg': 1000.0,
                'kilogram': 1000.0,
                'kilograms': 1000.0,
                'lb': 453.592,
                'pound': 453.592,
                'pounds': 453.592,
                'oz': 28.3495,
                'ounce': 28.3495,
                'ounces': 28.3495,
                'mg': 0.001,
                'milligram': 0.001,
                'milligrams': 0.001,
            },
            'temperature': {
                # Temperature conversions handled separately
                'celsius': 'celsius',
                'fahrenheit': 'fahrenheit',
                'kelvin': 'kelvin',
            }
        }

    def convert_units(self, quantity: float, from_unit: str, to_unit: str) -> Optional[float]:
        """Convert quantity from one unit to another"""
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()

        if from_unit == to_unit:
            return quantity

        # Find unit type
        unit_type = self._get_unit_type(from_unit)
        if not unit_type or unit_type != self._get_unit_type(to_unit):
            return None  # Incompatible units

        if unit_type == 'temperature':
            return self._convert_temperature(quantity, from_unit, to_unit)

        # Convert to standard unit, then to target unit
        conversion_table = self.conversion_table[unit_type]

        if from_unit not in conversion_table or to_unit not in conversion_table:
            return None

        # Convert to standard unit (ml for volume, g for weight)
        standard_quantity = quantity * conversion_table[from_unit]

        # Convert from standard unit to target unit
        target_quantity = standard_quantity / conversion_table[to_unit]

        return round(target_quantity, 3)

    def convert_to_standard_unit(self, quantity: float, unit: str) -> float:
        """Convert quantity to standard unit for comparison"""
        unit = unit.lower().strip()
        unit_type = self._get_unit_type(unit)

        if not unit_type:
            return quantity  # Unknown unit, return as-is

        if unit_type == 'temperature':
            return self._convert_temperature(quantity, unit, 'celsius')

        standard_unit = self.standard_units[unit_type]
        converted = self.convert_units(quantity, unit, standard_unit)

        return converted if converted is not None else quantity

    def _get_unit_type(self, unit: str) -> Optional[str]:
        """Determine the type of unit (volume, weight, temperature)"""
        unit = unit.lower().strip()

        for unit_type, units in self.conversion_table.items():
            if unit in units:
                return unit_type

        return None

    def _convert_temperature(self, quantity: float, from_unit: str, to_unit: str) -> float:
        """Convert temperature between different scales"""
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()

        if from_unit == to_unit:
            return quantity

        # Convert to Celsius first
        if from_unit == 'fahrenheit':
            celsius = (quantity - 32) * 5 / 9
        elif from_unit == 'kelvin':
            celsius = quantity - 273.15
        else:  # from_unit == 'celsius'
            celsius = quantity

        # Convert from Celsius to target unit
        if to_unit == 'fahrenheit':
            return celsius * 9 / 5 + 32
        elif to_unit == 'kelvin':
            return celsius + 273.15
        else:  # to_unit == 'celsius'
            return celsius

    def get_compatible_units(self, unit: str) -> List[str]:
        """Get list of units compatible with given unit"""
        unit_type = self._get_unit_type(unit.lower().strip())

        if unit_type:
            return list(self.conversion_table[unit_type].keys())

        return []

    def format_quantity(self, quantity: float, unit: str) -> str:
        """Format quantity with appropriate precision"""
        if quantity == int(quantity):
            return f"{int(quantity)} {unit}"
        elif quantity < 0.1:
            return f"{quantity:.3f} {unit}"
        elif quantity < 1:
            return f"{quantity:.2f} {unit}"
        else:
            return f"{quantity:.1f} {unit}"

    def are_units_compatible(self, unit1: str, unit2: str) -> bool:
        """Check if two units are compatible (can be converted)"""
        type1 = self._get_unit_type(unit1.lower().strip())
        type2 = self._get_unit_type(unit2.lower().strip())

        return type1 is not None and type1 == type2