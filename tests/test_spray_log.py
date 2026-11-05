from datetime import datetime

from pi_logic.spray_log import last_spray, record_spray


def test_last_spray_is_none_before_any_spray():
    assert last_spray() is None


def test_record_spray_formats_and_stores_the_time():
    entry = record_spray(datetime(2022, 3, 21, 15, 13, 20))

    assert entry == {"date": "03/21/22", "time": "15:13:20"}
    assert last_spray() == entry


def test_only_the_most_recent_spray_is_kept():
    record_spray(datetime(2022, 3, 21, 15, 13, 20))
    record_spray(datetime(2022, 3, 22, 9, 0, 0))

    assert last_spray() == {"date": "03/22/22", "time": "09:00:00"}
