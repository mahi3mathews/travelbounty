from app.weekly_sales import WeeklySales
from app.monthly_sales import MonthlySales
from app.daily_sales import DailySales


class BookingSalesByTime:
    def __init__(self):
        self.__daily_sales = DailySales()
        self.__weekly_sales = WeeklySales()
        self.__monthly_sales = MonthlySales()

    def get_daily_filter(self, key):
        return self.__daily_sales.get_filter(key)

    def get_weekly_filter(self, key):
        return self.__weekly_sales.get_filter(key)

    def get_monthly_filter(self, key):
        return self.__monthly_sales.get_filter(key)

    def get_daily_sales(self, bookings):
        return self.__daily_sales.calculate_sales(bookings)

    def get_weekly_sales(self, bookings):
        return self.__weekly_sales.calculate_sales(bookings)

    def get_monthly_sales(self, bookings):
        return self.__monthly_sales.calculate_sales(bookings)
