from app.booking_sales import BookingSales
from datetime import datetime, timedelta, date


class WeeklySales(BookingSales):
    def __init__(self):
        super().__init__()

    def calculate_sales(self, bookings):

        result = {"Mon": 0, "Tue": 0, "Wed": 0, "Thu": 0, "Fri": 0, "Sat": 0, "Sun": 0}
        for booking in bookings:
            b_date = str(booking["booking_date"])
            try:
                b_date_obj = datetime.strptime(b_date, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                if booking["booking_date"].microsecond != 0:
                    b_date_obj = datetime.strptime(b_date, '%Y-%m-%d %H:%M:%S.%f'[:-1])
                else:
                    b_date_obj = datetime.strptime(b_date, '%Y-%m-%d %H:%M:%S')

            b_day = b_date_obj.strftime("%a")
            if b_day in result:
                result[b_day] = result[b_day] + booking["total_price"]

        return result

    def get_filter(self, date_key):
        today = date.today()
        sat_offset = (today.weekday() - 5) % 7
        fri_offset = (4 - today.weekday()) % 7
        start_date = today - timedelta(days=sat_offset)
        end_date = today + timedelta(days=fri_offset)
        return {date_key: {"$gte": start_date, "$lt": end_date}}
