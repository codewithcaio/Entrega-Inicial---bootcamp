"""Testes de unidade puros de app/services/booking_service.py — sem DB, sem HTTP.

Cobre RN01 (conflito de horário) e o cálculo de disponibilidade (SPEC.md seção 4.4/6).
"""
from __future__ import annotations

from datetime import date, datetime, time

import pytest

from app.services import booking_service as svc


def dt(hour: int, minute: int = 0, day: int = 15) -> datetime:
    return datetime(2026, 9, day, hour, minute)


class TestHasConflict:
    def test_no_existing_bookings_never_conflicts(self):
        assert svc.has_conflict([], dt(10), dt(11)) is False

    def test_identical_interval_conflicts(self):
        existing = [svc.BookingInterval(start=dt(10), end=dt(11))]
        assert svc.has_conflict(existing, dt(10), dt(11)) is True

    def test_new_booking_fully_inside_existing_conflicts(self):
        existing = [svc.BookingInterval(start=dt(9), end=dt(12))]
        assert svc.has_conflict(existing, dt(10), dt(11)) is True

    def test_new_booking_fully_containing_existing_conflicts(self):
        existing = [svc.BookingInterval(start=dt(10), end=dt(11))]
        assert svc.has_conflict(existing, dt(9), dt(12)) is True

    def test_partial_overlap_start_conflicts(self):
        existing = [svc.BookingInterval(start=dt(10), end=dt(11))]
        assert svc.has_conflict(existing, dt(9, 30), dt(10, 30)) is True

    def test_partial_overlap_end_conflicts(self):
        existing = [svc.BookingInterval(start=dt(10), end=dt(11))]
        assert svc.has_conflict(existing, dt(10, 30), dt(11, 30)) is True

    def test_back_to_back_end_equals_start_does_not_conflict(self):
        """Edge case: uma reserva terminando às 11:00 não bloqueia uma começando às 11:00."""
        existing = [svc.BookingInterval(start=dt(10), end=dt(11))]
        assert svc.has_conflict(existing, dt(11), dt(12)) is False

    def test_back_to_back_before_does_not_conflict(self):
        existing = [svc.BookingInterval(start=dt(10), end=dt(11))]
        assert svc.has_conflict(existing, dt(9), dt(10)) is False

    def test_conflict_checked_against_multiple_existing_bookings(self):
        existing = [
            svc.BookingInterval(start=dt(9), end=dt(10)),
            svc.BookingInterval(start=dt(14), end=dt(15)),
        ]
        assert svc.has_conflict(existing, dt(13, 30), dt(14, 30)) is True
        assert svc.has_conflict(existing, dt(10), dt(14)) is False


class TestValidateInterval:
    def test_valid_interval_does_not_raise(self):
        svc.validate_interval(dt(10), dt(11))

    def test_end_before_start_raises(self):
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_interval(dt(11), dt(10))

    def test_end_equal_start_raises(self):
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_interval(dt(10), dt(10))

    def test_duration_below_minimum_raises(self):
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_interval(dt(10, 0), dt(10, 10))

    def test_duration_exactly_minimum_is_valid(self):
        svc.validate_interval(dt(10, 0), dt(10, 15))

    def test_duration_above_maximum_raises(self):
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_interval(dt(8, 0), dt(17, 0))  # 9h > máximo de 8h

    def test_duration_exactly_maximum_is_valid(self):
        svc.validate_interval(dt(8, 0), dt(16, 0))  # exatamente 8h


class TestValidateNotInPast:
    def test_future_start_does_not_raise(self):
        now = dt(9)
        svc.validate_not_in_past(dt(10), now)

    def test_past_start_raises(self):
        now = dt(10)
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_not_in_past(dt(9), now)

    def test_start_equal_now_is_valid(self):
        now = dt(10)
        svc.validate_not_in_past(dt(10), now)


class TestValidateBusinessHours:
    HOURS_START = time(8, 0)
    HOURS_END = time(20, 0)

    def test_inside_business_hours_does_not_raise(self):
        svc.validate_business_hours(dt(9), dt(10), self.HOURS_START, self.HOURS_END)

    def test_start_before_opening_raises(self):
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_business_hours(dt(7), dt(9), self.HOURS_START, self.HOURS_END)

    def test_end_after_closing_raises(self):
        """R-002 (docs/REFINEMENTS.md): end_time também precisa estar dentro do expediente."""
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_business_hours(dt(19, 30), dt(20, 30), self.HOURS_START, self.HOURS_END)

    def test_ending_exactly_at_closing_is_valid(self):
        svc.validate_business_hours(dt(19), dt(20), self.HOURS_START, self.HOURS_END)

    def test_spanning_two_days_raises(self):
        start = dt(23, day=15)
        end = dt(1, day=16)
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_business_hours(start, end, self.HOURS_START, self.HOURS_END)


class TestValidateCapacity:
    def test_within_capacity_does_not_raise(self):
        svc.validate_capacity(5, 8)

    def test_exactly_at_capacity_is_valid(self):
        svc.validate_capacity(8, 8)

    def test_above_capacity_raises(self):
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_capacity(9, 8)

    def test_zero_attendees_raises(self):
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_capacity(0, 8)

    def test_negative_attendees_raises(self):
        with pytest.raises(svc.BusinessRuleViolation):
            svc.validate_capacity(-1, 8)


class TestComputeAvailability:
    HOURS_START = time(8, 0)
    HOURS_END = time(20, 0)
    DAY = date(2026, 9, 15)

    def test_no_bookings_whole_day_is_free(self):
        slots = svc.compute_availability([], self.DAY, self.HOURS_START, self.HOURS_END)
        assert len(slots) == 1
        assert slots[0].start == datetime(2026, 9, 15, 8, 0)
        assert slots[0].end == datetime(2026, 9, 15, 20, 0)

    def test_single_booking_splits_day_in_two_slots(self):
        bookings = [svc.BookingInterval(start=dt(10), end=dt(11))]
        slots = svc.compute_availability(bookings, self.DAY, self.HOURS_START, self.HOURS_END)
        assert len(slots) == 2
        assert slots[0].start == dt(8) and slots[0].end == dt(10)
        assert slots[1].start == dt(11) and slots[1].end == dt(20)

    def test_booking_at_start_of_day_removes_first_slot(self):
        bookings = [svc.BookingInterval(start=dt(8), end=dt(9))]
        slots = svc.compute_availability(bookings, self.DAY, self.HOURS_START, self.HOURS_END)
        assert len(slots) == 1
        assert slots[0].start == dt(9)

    def test_booking_covering_whole_day_leaves_no_slots(self):
        bookings = [svc.BookingInterval(start=dt(8), end=dt(20))]
        slots = svc.compute_availability(bookings, self.DAY, self.HOURS_START, self.HOURS_END)
        assert slots == []

    def test_unordered_bookings_are_handled_correctly(self):
        bookings = [
            svc.BookingInterval(start=dt(14), end=dt(15)),
            svc.BookingInterval(start=dt(9), end=dt(10)),
        ]
        slots = svc.compute_availability(bookings, self.DAY, self.HOURS_START, self.HOURS_END)
        assert len(slots) == 3
        assert [ (s.start.hour, s.end.hour) for s in slots ] == [(8, 9), (10, 14), (15, 20)]
