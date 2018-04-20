from model import Crud

c = Crud()


def add_new(vehicle, expiry):
    add_item = c.add_new(vehicle, expiry)
    return add_item


def sort_all():
    sorted_list = c.sort_all()
    return list(sorted_list)


def sort_show_vehicle():
    sorted_list = c.sort_all()
    list_vehicle = []
    for row in sorted_list:
        list_vehicle.append(row[0])
    return list_vehicle


def show_within(dayarg):
    sorted_list = c.sort_within(dayarg)
    return sorted_list


def update_checks(vehicle, expiry, inform, inspect, renew):
    update_item = c.update_checks(vehicle, expiry, inform, inspect, renew)
    return update_item


def delete_item(vehicle):
    del_it = c.delete_item(vehicle)
    return del_it
