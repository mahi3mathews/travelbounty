from app.booking_sales import BookingSales
from datetime import datetime, time


class DailySales(BookingSales):
    def __init__(self):
        super().__init__()

    def calculate_sales(self, bookings):
        result = {"8am": 0, "9am": 0, "10am": 0, "11am": 0, "12pm": 0, "1pm": 0, "2pm": 0, "3pm": 0,
                  "4pm": 0, "5pm": 0, "6pm": 0}
        for booking in bookings:
            b_date = str(booking["booking_date"])
            try:
                b_date_obj = datetime.strptime(b_date, '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                if booking["booking_date"].microsecond != 0:
                    b_date_obj = datetime.strptime(b_date, '%Y-%m-%d %H:%M:%S.%f'[:-1])
                else:
                    b_date_obj = datetime.strptime(b_date, '%Y-%m-%d %H:%M:%S')
            b_day = b_date_obj.strftime('%#I%p').lower()
            if b_day in result:
                result[b_day] = result[b_day] + booking["total_price"]

        return result

    def get_filter(self, date_key):
        now = datetime.now()
        start_time = datetime.combine(now.date(), time(hour=8))
        end_time = datetime.combine(now.date(), time(hour=18))
        return {date_key: {"$gte": start_time, "$lt": end_time}}
