from django.db.models import Manager


class CarManager(Manager):
    def price_gt(self, price):
        return self.filter(price__gt=price)

    def cars_audi(self):
        return self.filter(brand='audi')
