import csv
import datetime as dt
import random
import sys
from datetime import date, datetime
from typing import List, Callable, Tuple

from model import Crud


"""
TODO:
    Add functions to export generated data directly to database
"""
class VehiculeGenerator:
    @staticmethod
    def gen_numbers() -> Tuple[List[int],List[int]]:

        gen_nums: List[int] = [random.randint(0, 9) for _ in range(4)]
        csnums: List[int] = [num * (5 - index) for index, num in enumerate(gen_nums)]

        return gen_nums, csnums

    @staticmethod
    def car_plate() -> str:
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

        a1 = ["S"]

        a2 = ["F", "J", "K", "L"]

        a3 = ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
              "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", ]

        gen_a1 = random.choice(a1)
        gen_a2 = random.choice(a2)
        gen_a3 = random.choice(a3)

        gen_nums, csnums = VehiculeGenerator.gen_numbers()

        prefix = gen_a1 + gen_a2 + gen_a3

        exception = "SKY"
        if prefix == exception: #TODO find solution for this edge case
            pass

        csalp2 = (ord(gen_a2.lower()) - 96) * 9
        csalp3 = (ord(gen_a3.lower()) - 96) * 4

        compute = csalp2 + csalp3 + sum(csnums)

        number = ''.join(str(num) for num in gen_nums)

        # TODO: Handle Value Error
        suffix = VehiculeGenerator.get_suffix(compute)

        compete = prefix + number + suffix
        return compete

    @staticmethod
    def goods_plate() -> str:
        """
        Generate commerical vehicle number plate

        """

        a1 = ["G"]

        a2 = ["T", "U", "V", "W", "X", "Y", "Z", "BA", "BB", "BC", "BD", "BE"]

        gen_a1 = random.choice(a1)
        gen_a2 = random.choice(a2)

        gen_nums, csnums = VehiculeGenerator.gen_numbers()

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
        suffix = VehiculeGenerator.get_suffix(compute)

        compete = prefix + number + suffix
        return compete

    @staticmethod
    def get_suffix(num) -> str:
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

    @staticmethod
    def date_gen() -> str:
        """
        Generate random date ranging from today and one year later
        """
        rd = random.randrange(0, 365)
        rod = dt.timedelta(days=rd)
        return datetime.strftime(date.today() + rod, '%d.%m.%Y')

    @staticmethod
    def generate(number, typeof=None) -> List[str]:
        """
        args:
            number --> number of vehicles to generate.

            typeof --> None to generate both commerical and cars randomly
                   --> "cars" for car only
                   --> "goods" for commerical vehicle only

        """
        generate_type = None
        cars: List[str] = []

        if not typeof:
            plate_generators: List[Callable] = [VehiculeGenerator.car_plate, VehiculeGenerator.goods_plate]
            random_int: int = random.randint(0, len(plate_generators)-1)
            generate_type = plate_generators[random_int]
        elif typeof == "cars":
            generate_type = VehiculeGenerator.car_plate
        else:
            generate_type = VehiculeGenerator.goods_plate

        for _ in range(number):
            new_license_plate: str = generate_type()
            cars.append(new_license_plate)

        return cars

    @staticmethod
    def csv_writer(entries, typeof=None):
        """
        write a list of random generated vehicle number and roadtax expiry date
        to a CSV file with filename as "roadtax.csv"

        args:
            refer to generate(number, typeof = None) for more info

        """
        with open('roadtax.csv', 'w+', newline='') as f:
            fieldnames = ['CarPlate', 'ExpiryDate']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            items = VehiculeGenerator.generate(entries, typeof)
            writer.writeheader()
            for item in items:
                writer.writerow(
                    {'CarPlate': f"{item}", 'ExpiryDate': f"{VehiculeGenerator.date_gen()}"})

    @staticmethod
    def database_upload(entries, typeof=None):
        """
        write a list of random generated vehicle number and roadtax expiry date
        to a SQlite3 database with filename as "roadtax_date.db" according to
        model.py

        args:
            refer to generate(number, typeof = None) for more info

        """
        c = Crud()
        items = VehiculeGenerator.generate(entries, typeof)
        for item in items:
            c.add_new(item, VehiculeGenerator.date_gen())

    @staticmethod
    def main():
        """
        running as a script.
            --> no arg provided, auto generate 100 random vehicle numbers
            --> number of vehicle number provided, generate number with random
                type
            --> number of vehicle and type provided, generate number with that
                named type. refer to generate function for typeof keywords
        """
        if len(sys.argv) == 2:
            VehiculeGenerator.generate(int(sys.argv[1]))
            input(
                f"{sys.argv[1]} random vehicle generated. Press any key to continue..")
        elif len(sys.argv) > 2:
            VehiculeGenerator.generate(int(sys.argv[1]), sys.argv[2])
            input(
                f"{sys.argv[1]} random vehicle generated. Press any key to continue..")
        else:
            VehiculeGenerator.generate(100)
            VehiculeGenerator.csv_writer(100) # Create csv file while generating values
            # Create Entries in Database(roadtax_date) table('vehicle') With the help of model class
            VehiculeGenerator.database_upload(100)
            input(f"{100} random vehicle generated. Press any key to continue..")


if __name__ == '__main__':
    VehiculeGenerator.main()
