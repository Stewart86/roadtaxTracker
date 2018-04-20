from model import Vehicle, Crud

## Create
def add_new(vehicle, expiry):
        add_item = Crud.add_new(vehicle, expiry)
        return add_item
                
        
## Read
def sort_all():
        sorted_list = Crud.sort_all()
        return list(sorted_list)

def sort_show_vehicle():
        sorted_list = Crud.sort_all()
        list_vehicle = []
        for row in sorted_list:
                list_vehicle.append(row[0])
        return list_vehicle

def show_within(dayarg):
        sorted_list = Crud.sort_within(dayarg)
        return sorted_list

## Update
def update_checks(vehicle, expiry, inform, inspect, renew):
        update_item = Crud.update_checks(vehicle, expiry, inform, inspect, renew)
        return update_item

## Delete
def delete_item(vehicle):
        del_it = Crud.delete_item(vehicle)
        return del_it
