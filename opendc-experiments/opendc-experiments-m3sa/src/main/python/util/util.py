UNIT_FACTORS: dict[int, str] = {
    -9: 'n',
    -6: 'μ',
    -3: 'm',
    0: '',
    1: 'k',
    3: 'M',
    6: 'G',
    9: 'T'
}


def adjust_unit(target_unit: str, magnitude: int) -> tuple[str, int]:
    """
    Adjusts the unit based on the magnitude provided.
    Example:
        adjust_unit('W', 3) -> ('kW', 1000)
    Args:
        target_unit: The target unit to adjust.
        magnitude: The magnitude to adjust the unit by.

    Returns:
        A tuple containing the adjusted unit and magnitude.
    """

    result_unit = UNIT_FACTORS.get(magnitude, '') + target_unit
    result_magnitude = (10 ** magnitude) if magnitude in UNIT_FACTORS else 1
    return result_unit, result_magnitude
