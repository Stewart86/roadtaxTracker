from peewee import Model, SqliteDatabase, CharField, DateField, BooleanField
from datetime import date, datetime
import datetime as dt


db = SqliteDatabase('roadtax_date.db')


class Vehicle(Model):
    vehicle_no = CharField(primary_key=True)
    expiry_date = DateField()
    is_informed = BooleanField(default=False)
    is_inspected = BooleanField(default=False)
    is_renewed = BooleanField(default=False)

    @classmethod
    def create(cls, vehicle_no, expiry_date):
        # WIP
        # parsed_date = None
        # super(vehicle_no=vehicle_no, expiry_date=_parse_date(expiry_date))
        return

    @staticmethod
    def _parse_date(date):
        if type(date) is datetime:
            return date
        try:
            return datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            return datetime.strptime(expiry, '%d.%m.%Y')
        raise ValueError("date format must be dd.mm.YYYY")

    class Meta:
        database = db


class Crud:
    def add_new(self, vehicle, expiry):
        try:
            self.parsed_date = datetime.strptime(expiry, '%d/%m/%Y')
            self.create_new = Vehicle.create(
                vehicle_no=vehicle, expiry_date=self.parsed_date)
            return "New record created"
        except ValueError:
            try:
                self.parsed_date = datetime.strptime(expiry, '%d.%m.%Y')
                self.create_new = Vehicle.create(
                    vehicle_no=vehicle, expiry_date=self.parsed_date)
                return "New record created"
            except:
                self.msg = "date format must be dd.mm.YYYY"
                return self.msg if vehicle else None

        except:
            self.update_row = (Vehicle
                               .update(expiry_date=self.parsed_date)
                               .where(Vehicle.vehicle_no == vehicle)
                               .execute())
            return "Attempting to make change to existing vehicle."
        finally:
            db.close()

    def sort_all(self):
        self.query_orderby = Vehicle.select().order_by(Vehicle.expiry_date)
        self.display = []
        for item in self.query_orderby:
            self.display.append([item.vehicle_no, item.expiry_date, item.is_informed,
                                 item.is_inspected, item.is_renewed])
        db.close()
        return list(self.display)

    def sort_within(self, day):
        self.day = 1 if day == '' else day
        self.withindays = dt.timedelta(days=int(self.day))
        self.display = []
        self.query_within_days = Vehicle.select().where(Vehicle.expiry_date <=
                                                        date.today() + self.withindays).order_by(Vehicle.expiry_date)
        for item in self.query_within_days:
            self.display.append([item.vehicle_no, date.strftime(item.expiry_date, '%d/%m/%Y'), item.is_informed,
                                 item.is_inspected, item.is_renewed])
        db.close()
        return self.display

    def update_checks(self,
                      vehicle,
                      expiry,
                      inform=False,
                      inspect=False,
                      renew=False):
        if vehicle is None:
            return None
        try:
            self.parsed_date = datetime.strptime(expiry, '%d/%m/%Y')
        except:
            pass
        self.update_row = (Vehicle
                           .update(is_informed=inform,
                                   is_inspected=inspect,
                                   is_renewed=renew,
                                   expiry_date=self.parsed_date + dt.timedelta(days=182.5))
                           .where(Vehicle.vehicle_no == vehicle)
                           .execute())
        db.close()
        if inform and inspect and renew:
            return f"{vehicle} renewed, expiry date updated to 6 months from now."
        return = f"{vehicle} updated"

    def delete_item(self, vehicle):
        if vehicle is None:
            return None
        self.del_it = Vehicle.delete().where(Vehicle.vehicle_no == vehicle).execute()
        db.close()
        return f"{vehicle} Deleted!"


db.connect()
db.create_tables([Vehicle])
db.close()
