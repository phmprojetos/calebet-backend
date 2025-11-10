"""Helpers for resolving date range filters used by the API."""

from __future__ import annotations

from datetime import datetime, time, timedelta
from typing import Optional, Tuple

DateRange = Optional[Tuple[datetime, datetime]]


def _parse_start(date_str: str) -> datetime:
    dt = datetime.fromisoformat(date_str)
    if dt.time() == time(0, 0):
        return datetime.combine(dt.date(), time.min)
    return dt


def _parse_end(date_str: str) -> datetime:
    dt = datetime.fromisoformat(date_str)
    if dt.time() == time(0, 0):
        return datetime.combine(dt.date(), time.max)
    return dt


def resolve_date_range(
    filter: Optional[str], start_date: Optional[str], end_date: Optional[str]
) -> DateRange:
    """Resolve the provided filter arguments into a datetime range."""

    if start_date and end_date:
        return _parse_start(start_date), _parse_end(end_date)

    now = datetime.now()

    if filter == "today":
        start = datetime.combine(now.date(), time.min)
        end = datetime.combine(now.date(), time.max)
        return start, end

    if filter == "7days":
        return now - timedelta(days=7), now

    if filter == "30days":
        return now - timedelta(days=30), now

    if filter == "all" or filter is None:
        return None

    return None
