from datetime import datetime


class DateParser:
    """업데이트 가능한 Date 컬렉터로서
    지정된 format과 frequency정보에 따라 표준포맷(frequency에 따라 y:%Y, m:%Y%m, d:%Y%m%d)으로 값을 리턴하며,
    업데이트 될때마다 최종 날짜와 최초날짜를 기록한다.
    """

    def __init__(self, format, frequency):
        self.format = format
        self.frequency = frequency
        self.last_date = "0"
        self.first_date = "99999999"

    def _update_last_date(self):
        if self.last_date < self.current_date:
            self.last_date = self.current_date
        if self.first_date > self.current_date:
            self.first_date = self.current_date

    def _parse_date(self, datestr):
        option = self.frequency.lower()
        date_obj = datetime.strptime(datestr, self.format)
        if option == "y":
            self.current_date = date_obj.strftime("%Y")
        elif option == "m":
            self.current_date = date_obj.strftime("%Y%m")
        else:
            self.current_date = date_obj.strftime("%Y%m%d")
        self._update_last_date()

    def update(self, datestr):
        self._parse_date(datestr)

    def get(self):
        return self.current_date

    def get_year(self):
        if self.current_date and len(self.current_date) >= 4:
            return self.current_date[:4]

    def get_month(self):
        if self.current_date and len(self.current_date) >= 6:
            return self.current_date[4:6]

    def get_day(self):
        if self.current_date and len(self.current_date) >= 8:
            return self.current_date[6:]

import uuid
class LastDateCollector:
    """최종날짜만 기록하는 컬렉터
    """

    _last_date = '00000000'

    def force_set_date(self, date):
        self._last_date = date

    def update(self, current_date):
        if self._last_date < current_date:
            self._last_date = current_date

    def get(self):
        return self._last_date