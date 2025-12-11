"""
A utility module for paginated data operations.

This module provides functions for calculating the offset for paginated
data and ensuring that provided limits do not exceed a maximum allowed
value.
"""


def compute_offset(page: int, limit: int) -> int:
    """
    Calculate the offset for pagination based on the current page and the limit.

    This function is typically used to determine the starting point of records in a
    paged dataset by converting the current page number and the limit of items per
    page into an offset.

    Params:
        page (int): Current page number for pagination.
        limit (int): Number of items per page for pagination.
                inclusive.
    Returns:
        Page (int): The calculated offset for pagination.
    """
    offset = (page - 1) * limit
    return offset


def clamp_limit(limit: int, max_limit: int) -> int:
    """
    Clamp the provided limit to a maximum value.

    This function compares the given `limit` to the `max_limit` and returns the
    smaller of the two. It is intended to ensure that `limit` does not exceed
    the specified `max_limit`.

    Param:
     limit: The value to be clamped.
    max_limit: The upper limit to clamp the value to.
    Return: The clamped value, which is the smaller of `limit` and `max_limit`.

    """
    return min(limit, max_limit)
