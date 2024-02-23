import unittest

from vehicleGen import VehiculeGenerator


class TestVehicleNumber(unittest.TestCase):
    #Test vehicle Number generation

    def test_gen_numbers(self):
        gen_nums, csnums = VehiculeGenerator.gen_numbers()
        self.assertEqual(8,len(gen_nums)+len(csnums))

    def test_goods_plate(self):
        self.assertEqual(VehiculeGenerator.goods_plate()[0], "G")

    def test_car_plate(self):
        self.assertEqual(VehiculeGenerator.car_plate()[0], "S")

    def test_generate(self):
        test1 = VehiculeGenerator.generate(100, "cars")
        test2 = VehiculeGenerator.generate(100, "goods")
        self.assertEqual(len(test1), 100)
        self.assertEqual(len(test2), 100)
        for i in test1:
            self.assertEqual(i[0], "S")
        for i in test2:
            self.assertEqual(i[0], "G")

    def test_exception(self):
        test1 = VehiculeGenerator.generate(200, "cars")
        for item in test1:
            self.assertNotEqual(item[0:4], "SKY")

    def test_checksum(self):
        test1 = VehiculeGenerator.generate(100)
        for item in test1:
            if len(item) == 8:
                compute = (
                    ((ord(item[1].lower())-96) * 9) +
                    ((ord(item[2].lower())-96) * 4) +
                    (int(item[3]) * 5) +
                    (int(item[4]) * 4) +
                    (int(item[5]) * 3) +
                    (int(item[6]) * 2))
                checksum = compute % 19
                letters = "AZYXUTSRPMLKJHGEDCB"
                self.assertEqual(item[7], letters[checksum])
            else:
                compute = (
                    ((ord(item[0].lower())-96) * 9) +
                    ((ord(item[1].lower())-96) * 4) +
                    (int(item[2]) * 5) +
                    (int(item[3]) * 4) +
                    (int(item[4]) * 3) +
                    (int(item[5]) * 2))
                checksum = compute % 19
                letters = "AZYXUTSRPMLKJHGEDCB"
                self.assertEqual(item[6], letters[checksum])
