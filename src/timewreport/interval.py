import dateutil.parser

from datetime import datetime, date
from dateutil.tz import tz


class TimeWarriorInterval(object):
    def __init__(self, start, end, tags):
        self.__start: datetime = self.__get_local_datetime(start)
        self.__end: datetime = self.__get_local_datetime(end)
        self.__tags = tags

    def __eq__(self, other):
        return (
            self.__start == other.get_start()
            and self.__end == other.get_end()
            and self.__tags == other.get_tags()
        )

    def __hash__(self):
        return hash(repr(self))

    def get_start(self):
        return self.__start

    def get_end(self):
        return self.__end

    def get_tags(self):
        return self.__tags

    def is_open(self) -> bool:
        return self.__end is None

    def get_duration(self) -> datetime:
        if self.is_open():
            return datetime.now(tz=tz.local()) - self.__start
        else:
            return self.__end - self.__start

    def get_date(self):
        return date(self.__start.year, self.__start.month, self.__start.day)

    def __get_local_datetime(self, datetime_str: str) -> datetime:
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        date = dateutil.parser.parse(datetime_str)
        date.replace(tzinfo=from_zone)

        return date.astimezone(to_zone)


def get_local_datetime(datetime_str: str):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    date = dateutil.parser.parse(datetime_str)
    date.replace(tzinfo=from_zone)

    return date.astimezone(to_zone)
