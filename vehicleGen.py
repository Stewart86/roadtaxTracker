import csv
import datetime as dt
import random
import argparse
from datetime import date, datetime

from model import Crud


"""
TODO:
    Add functions to export generated data directly to database
"""

def gen_numbers():
    gen_nums = []
    csnums = []
    for i in range(4):
        gen_nums.append(random.randrange(10))
        csnums.append(gen_nums[i] * (5-i))
    return gen_nums, csnums


def car_plate():
    """
    Generate passenger vehicle number plate

    Checksum:

    where A=1 and Z=26,

    Each individual number is then multiplied
    by 6 fixed numbers (9, 4, 5, 4, 3, 2)

    These are added up, then divided by 19.

    19 letters used
    (A, Z, Y, X, U, T, S, R, P, M, L, K, J, H, G, E, D, C, B)
    with "A" corresponding to a remainder of 0,
    "Z" corresponding to 1, "Y" corresponding to 2 and so on

    """

    a1 = "S"

    a2 = ["F", "J", "K", "L"]

    a3 = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
          "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ]

    gen_a1 = random.choice(a1)
    gen_a2 = random.choice(a2)
    gen_a3 = random.choice(a3)

    gen_nums, csnums = gen_numbers()

    prefix = gen_a1 + gen_a2 + gen_a3

    # QUESTION: What was the point of this?
    # As the script would behave exactly the same if we left it out.
    # If the goal is to exclude 'SKY' results, then don't "pass".
    # I fixed it in the generate function.
    #
    # exception = "SKY"
    # if prefix == exception:
    #    pass

    csalp2 = (ord(gen_a2.lower()) - 96) * 9
    csalp3 = (ord(gen_a3.lower()) - 96) * 4

    compute = csalp2 + csalp3 + sum(csnums)

    number = ''.join(str(num) for num in gen_nums)

    # TODO: Handle Value Error
    # QUESTION: What is meant by this?
    # QUESTION2: If we handle ValueError, shouldn't we do that in get_suffix?
    suffix = get_suffix(compute)

    compete = prefix + number + suffix
    return compete


def goods_plate():
    """
    Generate commerical vehicle number plate

    """

    a1 = "G"

    a2 = ["T", "U", "V", "W", "X", "Y", "Z", "BA", "BB", "BC", "BD", "BE"]

    gen_a1 = random.choice(a1)
    gen_a2 = random.choice(a2)

    gen_nums, csnums = gen_numbers()

    prefix = gen_a1 + gen_a2

    csalp2 = 0
    csalp3 = 0

    if len(prefix) == 2:

        csalp2 = (ord(prefix[0].lower()) - 96) * 9
        csalp3 = (ord(prefix[1].lower()) - 96) * 4

    else:
        csalp2 = (ord(prefix[1].lower()) - 96) * 9
        csalp3 = (ord(prefix[2].lower()) - 96) * 4

    compute = csalp2 + csalp3 + sum(csnums)

    number = ''.join(str(num) for num in gen_nums)

    # TODO: Handle Value Error 
    suffix = get_suffix(compute)

    compete = prefix + number + suffix
    return compete

def get_suffix(num):
    compute_dict = {   
        0  : 'A',
        1  : 'Z',
        2  : 'Y',
        3  : 'X',
        4  : 'U',
        5  : 'T',
        6  : 'S',
        7  : 'R',
        8  : 'P',
        9  : 'M',
        10 : 'L',
        11 : 'K',
        12 : 'J',
        13 : 'H',
        14 : 'G',
        15 : 'E',
        16 : 'D',
        17 : 'C',
        18 : 'B'
    }

    if num % 19 in compute_dict:
        return compute_dict[num % 19]
    else:
        raise ValueError


def date_gen():
    """
    Generate random date ranging from today and one year later
    """
    rd = random.randrange(0, 365)
    rod = dt.timedelta(days=rd)
    return datetime.strftime(date.today() + rod, '%d.%m.%Y')


def generate(number, typeof=None):
    """
    args:
        number --> number of vehicles to generate.

        typeof --> None to generate both commerical and cars randomly
               --> "cars" for car only
               --> "goods" for commerical vehicle only

    """
    list_of_cars = []

    if typeof is None:
        plate_generators = [car_plate, goods_plate]
        random_int = random.randint(0, len(plate_generators)-1)
        generate_type = plate_generators[random_int]
    elif typeof == "cars":
        generate_type = car_plate
    else:
        generate_type = goods_plate

    for _ in range(number):
        new_license_plate = generate_type()
        check_pass = False
        while not check_pass:
            try:
                assert new_license_plate[:3] != "SKY"
                check_pass = True
            except AssertionError:
                new_license_plate = generate_type()
        list_of_cars.append(new_license_plate)

    return list_of_cars


def csv_writer(entries, typeof=None):
    """
    Write a list of random generated vehicle number and roadtax expiry date
    to a CSV file with filename as "roadtax.csv"

    args:
        Refer to generate(number, typeof = None) for more info

    """
    with open('roadtax.csv', 'w', newline='') as f:
        fieldnames = ['CarPlate', 'ExpiryDate']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        items = generate(entries, typeof)
        writer.writeheader()
        for item in items:
            writer.writerow(
                {'CarPlate': f"{item}", 'ExpiryDate': f"{date_gen()}"})


def database_upload(entries, typeof=None):
    """
    Write a list of random generated vehicle number and roadtax expiry date
    to a SQlite3 database with filename as "roadtax_date.db" according to
    model.py

    Args:
        refer to generate(number, typeof = None) for more info

    """
    c = Crud()
    items = generate(entries, typeof)
    for item in items:
        c.add_new(item, date_gen())


def main():
    """
    Running as a script.
        --> No arg provided, auto generate 100 random vehicle numbers
        --> Number of vehicle number provided, generate number with random
            type
        --> Number of vehicle and type provided, generate number with that
            named type. Refer to generate function for typeof keywords
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n","--number", default=100, type=int,
                    help="Amount of vehicle numbers to generate, default 100")
    parser.add_argument("--type", choices=['cars', 'goods'],
                    help="Type of vehicle to create vehicle numbers for")
    args = parser.parse_args()

    if args.type:
        generate(args.number, args.type)
        result = (f"{args.number} vehicle numbers "
                 f"of type {args.type} generated. ")
    else:
        generate(args.number)
        result = f"{args.number} random vehicle numbers generated. "
    input(result+"Press Return to continue..")


if __name__ == '__main__':
    main()
