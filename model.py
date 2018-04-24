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

    class Meta:
        database = db


class Crud:
    def add_new(self, vehicle, expiry):
        try:
            self.parse_date = datetime.strptime(expiry, '%d/%m/%Y')
            self.create_new = Vehicle.create(
                vehicle_no=vehicle, expiry_date=self.parse_date)
            db.close()
            return "New record created"
        except ValueError:
            try:
                self.parse_date = datetime.strptime(expiry, '%d.%m.%Y')
                self.create_new = Vehicle.create(
                    vehicle_no=vehicle, expiry_date=self.parse_date)
                db.close()
                return "New record created"
            except:
                self.msg = "date format must be dd.mm.YYYY"
                db.close()
                return self.msg if vehicle else None

        except:
            self.update_row = (Vehicle
                               .update(expiry_date=self.parse_date)
                               .where(Vehicle.vehicle_no == vehicle)
                               .execute())
            db.close()
            return "Attempting to make change to existing vehicle."

    def sort_all(self):
        self.query_orderby = Vehicle.select().order_by(Vehicle.expiry_date)
        self.display = []
        for item in self.query_orderby:
            self.display.append([item.vehicle_no, item.expiry_date, item.is_informed,
                                 item.is_inspected, item.is_renewed])
        db.close()
        return list(self.display)

    def sort_within(self, dayarg):
        self.day = 1 if dayarg == '' else dayarg
        self.withindays = dt.timedelta(days=int(self.day))
        self.display = []
        self.query_within_days = Vehicle.select().where(Vehicle.expiry_date <=
                                                        date.today() + self.withindays).order_by(Vehicle.expiry_date)
        for item in self.query_within_days:
            self.display.append([item.vehicle_no, date.strftime(item.expiry_date, '%d/%m/%Y'), item.is_informed,
                                 item.is_inspected, item.is_renewed])
        db.close()
        return self.display if self.day else None

    def update_checks(self, vehicle, expiry, inform, inspect, renew):
        try:
            self.parse_date = datetime.strptime(expiry, '%d/%m/%Y')
        except:
            pass
        if inform and inspect and renew:
            self.update_row = (Vehicle
                               .update(is_informed=False,
                                       is_inspected=False,
                                       is_renewed=False,
                                       expiry_date=self.parse_date + dt.timedelta(days=182.5))
                               .where(Vehicle.vehicle_no == vehicle)
                               .execute())
            self.strMsg = f"{vehicle} renewed, expiry date updated to next 6 months"
        else:
            self.update_row = (Vehicle
                               .update(is_informed=inform,
                                       is_inspected=inspect,
                                       is_renewed=renew)
                               .where(Vehicle.vehicle_no == vehicle)
                               .execute())
            self.strMsg = f"{vehicle} updated"
        db.close()
        return self.strMsg if vehicle else None

    def delete_item(self, vehicle):
        self.del_it = Vehicle.delete().where(Vehicle.vehicle_no == vehicle).execute()
        self.strMsg = f"{vehicle} Deleted!"
        db.close()
        return self.strMsg if vehicle else None


db.connect()
db.create_tables([Vehicle])
db.close()
