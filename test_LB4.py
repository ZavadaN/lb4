import re
import inspect
import LB3

import unittest

class Test_Calculator(unittest.TestCase):

    def test_init(self, init_limit, msg_err):
        self.assertEqual(LB3, 'Calculator'), msg_err('add_class', 'Calculator')
        result = LB3.Calculator(init_limit)
        self.assertEqual(result, 'limit'), msg_err('add_attr', 'limit', 'Calculator')
        self.assertEqualresult.limit == init_limit, msg_err('wrong_attr', 'limit', 'Calculator')
        self.assertEqual(result, 'records'), msg_err('add_attr', 'records', 'Calculator')
        self.result.records == [], msg_err('wrong_attr', 'records', 'Calculator')

        assertFalse(result, 'USD_RATE'), msg_err('dont_create_attr', 'USD_RATE', 'Calculator')
        assertFalse(result, 'EURO_RATE'), msg_err('dont_create_attr', 'EURO_RATE', 'Calculator')

    def test_add_record(self, init_limit, data_records, msg_err):
        result = LB3.Calculator(init_limit)
        self.assertEqual(result, 'add_record'), msg_err('add_method', 'add_record', 'Calculator')
        records, today, week = data_records
        for record in records:
            result.add_record(record)
        self.assertEqualresult.records == records, msg_err('wrong_attr', 'records', 'Calculator')

    def test_get_today_stats(self, init_limit, data_records, msg_err):
        result = LB3.Calculator(init_limit)
        records, today, week = data_records
        for record in records:
            result.add_record(record)
        self.assertEqual(result, 'get_today_stats'), msg_err('add_method', 'get_today_stats', 'Calculator')
        self.assertEqualresult.get_today_stats() == today, msg_err('wrong_method', 'get_today_stats', 'Calculator')

    def test_get_week_stats(self, init_limit, data_records, msg_err):
        result = LB3.Calculator(init_limit)
        records, today, week = data_records
        for record in records:
            result.add_record(record)
        self.assertEqual(result, 'get_week_stats'), msg_err('add_method', 'get_week_stats', 'Calculator')
        self.assertEqualresult.get_week_stats() == week, msg_err('wrong_method', 'get_week_stats', 'Calculator')
        get_week_stats_inspect = inspect.getsource(result.get_week_stats)
        get_week_stats_inspect_in_class = inspect.getsource(LB3.Calculator)
        self.assertEqual(
            'days=7' in get_week_stats_inspect or
            'weeks=1' in get_week_stats_inspect or
            'days=7' in get_week_stats_inspect_in_class or
            'weeks=1' in get_week_stats_inspect_in_class
        ), 'Нужно считать, сколько денег было потрачено за неделю'

    def test_get_calories_remained(self, init_limit, msg_err):
        result = LB3.Calculator(init_limit)
        assert not hasattr(result, 'get_calories_remained'), (
            msg_err('dont_create_method', 'get_calories_remained', 'Calculator')
        )

    def test_get_today_cash_remained(self, init_limit, msg_err):
        result = LB3.Calculator(init_limit)
        assert not hasattr(result, 'get_today_cash_remained'), (
            msg_err('dont_create_method', 'get_today_cash_remained', 'Calculator')
        )



class Test_CashCalculator(unittest.TestCase)::

    def test_init(self, init_limit, msg_err):
        assert hasattr(LB3, 'CashCalculator'), (
            msg_err('add_class', 'CashCalculator', child=True, parent_name='Calculator')
        )
        result = LB3.CashCalculator(init_limit)
        assert hasattr(result, 'limit'), msg_err('child_method', 'CashCalculator', 'Calculator')
        assert result.limit == init_limit, msg_err('child_method', 'CashCalculator', 'Calculator')

        assert hasattr(result, 'EURO_RATE'), msg_err('add_attr', 'EURO_RATE', 'CashCalculator')
        assert type(result.EURO_RATE) == float, msg_err('wrong_attr', 'EURO_RATE', 'CashCalculator')
        assert result.EURO_RATE > 0, msg_err('wrong_attr', 'EURO_RATE', 'CashCalculator',
                                             msg=', курс не может быть равен или меньше 0')

        assert hasattr(result, 'USD_RATE'), msg_err('add_attr', 'USD_RATE', 'CashCalculator')
        assert type(result.USD_RATE) == float, msg_err('wrong_attr', 'USD_RATE', 'CashCalculator')
        assert result.USD_RATE > 0, msg_err('wrong_attr', 'USD_RATE', 'CashCalculator',
                                            msg=', курс не может быть равен или меньше 0')

    @pytest.mark.parametrize("amount,currency", [
        (0, 'usd'), (0, 'eur'), (0, 'rub'),
        (1, 'usd'), (1, 'eur'), (1, 'rub'),
        (-1, 'usd'), (-1, 'eur'), (-1, 'rub')
    ])
    def test_get_today_cash_remained(self, init_limit, data_records, amount, currency, today_cash_remained, msg_err,
                                     monkeypatch):
        result = LB3.CashCalculator(init_limit)
        assert hasattr(result, 'get_today_cash_remained'), (
            msg_err('add_method', 'get_today_cash_remained', 'CashCalculator')
        )

        records, today, week = data_records
        for record in records:
            result.add_record(record)

        result.EURO_RATE = 56
        monkeypatch.setattr(LB3.CashCalculator, "EURO_RATE", 56)
        result.USD_RATE = 58
        monkeypatch.setattr(LB3.CashCalculator, "USD_RATE", 58)
        result.limit = today + (amount * 300)
        assert re.fullmatch(today_cash_remained(amount, currency), result.get_today_cash_remained(currency)), (
            msg_err('wrong_method', 'get_today_cash_remained', 'CashCalculator')
        )