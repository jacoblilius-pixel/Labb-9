import unittest
from labb9 import readformel, molekyl, num, readatom, Syntaxfel


class Test1(unittest.TestCase):

    def test_molekyl(self):
        ordkö = molekyl("Si(C3(COOH)2)4(H2O)7")
        readformel(ordkö)
        self.assertTrue(ordkö.isEmpty())

    def test_felaktig(self):
        ordkö = molekyl("na")
        with self.assertRaises(Syntaxfel):
            readformel(ordkö)

    def test_första_bokstav(self):
        """Test att rätt felmeddelande lyfts vid Syntaxfel"""
        ordkö = molekyl("a")
        with self.assertRaises(Syntaxfel) as fel:
            readformel(ordkö)
        felet = fel.exception
        self.assertEqual(str(felet), "Saknad stor bokstav vid radslutet")

    def test_H2O(self):
        ordkö = molekyl("H2O")
        readformel(ordkö)
        self.assertTrue(ordkö.isEmpty())


class Test2(unittest.TestCase):
    def test_okänd_atom(self):
        ordkö = molekyl("C(Xx4)5")
        with self.assertRaises(Syntaxfel) as fel:
            readformel(ordkö)
        felet = fel.exception
        self.assertEqual(str(felet), "Okänd atom vid radslutet")

    def test_num(self):
        ordkö = molekyl("02")
        with self.assertRaises(Syntaxfel) as fel:
            num(ordkö)
        felet = fel.exception
        self.assertEqual(str(felet), "För litet tal vid radslutet")

    def test_H20Fe(self):
        ordkö = molekyl("H2O)Fe")
        with self.assertRaises(Syntaxfel):
            readformel(ordkö)

    def test_gruppstart(self):
        indata = [")", "2", "(Cl)2)3"]
        for värde in indata:
            ordkö = molekyl(värde)
            with self.assertRaises(Syntaxfel) as fel:
                readformel(ordkö)
                felet = fel.exception
                self.assertEqual(str(felet), "Felaktig gruppstart vid radslutet")

    def test_gilltig_atom(self):
        ordkö = molekyl("Nv")
        with self.assertRaises(Syntaxfel):
            readatom(ordkö)

    def test_fel_kö(self):
        ordkö = molekyl("Nacl")
        with self.assertRaises(Syntaxfel) as fel:
            readformel(ordkö)
            felet = fel.exception
            self.assertEqual(str(felet), "Saknad stor bokstav vid radslutet")
        self.assertFalse(ordkö.isEmpty())


if __name__ == "__main__":
    unittest.main()