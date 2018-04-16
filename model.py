from peewee import *
from datetime import date, datetime
import datetime as dt


db = SqliteDatabase('roadtax_date.db')

class Vehicle(Model):
    vehicle_no = CharField(primary_key = True)
    expiry_date = DateField()
    is_informed = BooleanField(default = False)
    is_inspected = BooleanField(default = False)
    is_renewed = BooleanField(default = False)

    class Meta:
        database = db

class Crud():
    ## Create
    def add_new(vehicle, expiry):
            try:
                parse_date = datetime.strptime(expiry, '%d.%m.%Y')
                create_new = Vehicle.create(vehicle_no = vehicle, expiry_date = parse_date)
                return "New record created"
            except ValueError as ve:
                msg = "date format must be dd.mm.YYYY"
                return msg if vehicle else None
                    
            except:
                update_row = (Vehicle
                              .update(expiry_date = parse_date)
                              .where(Vehicle.vehicle_no == vehicle)
                              .execute())
                return "Attempting to make change to existing vehicle."
                    
            
    ## Read
    def sort_all():
            query_orderby = Vehicle.select().order_by(Vehicle.expiry_date)
            display = []
            for item in query_orderby:            
                display.append([item.vehicle_no, item.expiry_date, item.is_informed,
                                item.is_inspected, item.is_renewed])
            return list(display)

    def sort_within(dayarg):
            day = 1 if dayarg == '' else dayarg
            withindays = dt.timedelta(days = int(day)) 
            display = []
            query_within_days = Vehicle.select().where(Vehicle.expiry_date <= date.today() + withindays)
            for item in query_within_days:
                    display.append([item.vehicle_no, date.strftime(item.expiry_date, '%d/%m/%Y'), item.is_informed,
                                    item.is_inspected, item.is_renewed])
            return display if day else None

    ## Update
    def update_checks(vehicle, expiry, inform, inspect, renew):
            try:
                parse_date = datetime.strptime(expiry, '%d/%m/%Y')
            except:
                pass
            if inform and inspect and renew:
                update_row = (Vehicle
                              .update(is_informed = False,
                                      is_inspected = False,
                                      is_renewed = False,
                                      expiry_date = parse_date + dt.timedelta(days = 182.5))
                              .where(Vehicle.vehicle_no == vehicle)
                              .execute())
                strMsg = f"{vehicle} renewed, expiry date updated to next 6 months"
            else:
                update_row = (Vehicle
                              .update(is_informed = inform,
                                     is_inspected = inspect,
                                     is_renewed = renew)
                              .where(Vehicle.vehicle_no == vehicle)
                              .execute())
                strMsg = f"{vehicle} updated"
            return strMsg if vehicle else None

    ## Delete
    def delete_item(vehicle):
            del_it = Vehicle.delete().where(Vehicle.vehicle_no == vehicle).execute()
            strMsg = f"{vehicle} Deleted!"
            return strMsg if vehicle else None

db.connect()
db.create_tables([Vehicle])
db.close()

