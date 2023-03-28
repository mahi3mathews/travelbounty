from app.booking_sales import BookingSales
from datetime import datetime


class MonthlySales(BookingSales):
    def __init__(self):
        super().__init__()

    def calculate_sales(self, bookings):
        result = {"Jan": 0, "Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0,
                  "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}
        for booking in bookings:
            b_date = str(booking["booking_date"])
            try:
                b_date_obj = datetime.strptime(b_date, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                if booking["booking_date"].microsecond != 0:
                    b_date_obj = datetime.strptime(b_date, '%Y-%m-%d %H:%M:%S.%f'[:-1])
                else:
                    b_date_obj = datetime.strptime(b_date, '%Y-%m-%d %H:%M:%S')
            b_day = b_date_obj.strftime("%b")
            if b_day in result:
                result[b_day] = result[b_day] + booking["total_price"]

        return result

    def get_filter(self, date_key):
        current_year = datetime.now().year
        start_date = datetime(current_year, 1, 1)
        end_date = datetime(current_year, 12, 31)
        return {date_key: {"$gte": start_date, "$lte": end_date}}
