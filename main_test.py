import unittest
from main import Header, Transaction, Footer


class TestHandleMethods(unittest.TestCase):

    def test_equal_headers(self):
        # create instance of header
        # transform to text
        # parse text to header
        # old header and new header must be equal
        header = Header(name="Ola", surname="Nowak",
                        patronymic="Marta", address="Grzybowska")
        new_header = Header.from_text(header.to_text())
        self.assertEqual(header, new_header)

    def test_expect_exception(self):
        with self.assertRaises(ValueError) as context:
            header = Header(name="a"*29, surname="v",
                            patronymic="q", address="m")
        with self.assertRaises(ValueError) as context:
            header = Header(name="a", surname="v"*31,
                            patronymic="x", address="k")
        with self.assertRaises(ValueError) as context:
            header = Header(name="a", surname="v",
                            patronymic="u"*31, address="j")
        with self.assertRaises(ValueError) as context:
            header = Header(name="a", surname="v",
                            patronymic="b", address="d"*31)

    def test_max_allowed_values(self):
        header = Header(name="a"*28, surname="b"*30,
                        patronymic="c"*30, address="d"*30)
        self.assertEqual(len(header.to_text()), 120)
        
class TestTransactionMethods(unittest.TestCase):

    def test_equal_transaction(self):
        transaction = Transaction(counter="000001", amount=2000, currency="PLN")
        new_transaction = Transaction.from_text(transaction.to_text())
        self.assertEqual(transaction, new_transaction)

    def test_expect_exception(self):
        with self.assertRaises(ValueError) as context:
            transaction = Transaction(counter="a"*7, amount="b", currency="PLN")
        with self.assertRaises(ValueError) as context:
            transaction = Transaction(counter="a", amount="b"*13, currency="PLN")
        with self.assertRaises(ValueError) as context:
            transaction = Transaction(counter="a", amount="b", currency="PLNS")
            
    def test_max_allowed_values(self):
        transaction = Transaction(counter="a"*6, amount=12,
                        currency="c"*3)
        self.assertEqual(len(transaction.to_text()), 120)

class TestFooterMethods(unittest.TestCase):

    def test_equal_footer(self):
        footer = Footer(total_counter=123, control_sum=2000)
        new_footer = Footer.from_text(footer.to_text())
        self.assertEqual(footer, new_footer)

    def test_expect_exception(self):
        with self.assertRaises(ValueError) as context:
            footer = Footer(total_counter=7, control_sum=12)
        with self.assertRaises(ValueError) as context:
            footer = Footer(total_counter=6, control_sum=13)
        

    def test_max_allowed_values(self):
        footer = Footer(total_counter=6, control_sum=12)
        self.assertEqual(len(footer.to_text()), 120)

if __name__ == '__main__':
    unittest.main()
