class NumberUtils():
    '''This functions works with the list comprehesion and catches only the prime numbers'''

    @staticmethod
    def is_prime(number: int) -> bool:

        if number > 1:
            for i in range(2, int(number / 2) + 1):
                if (number % i) == 0:
                    return False
            return True
        return False

    '''I need this function because the "random" module in rsa2 file somethimes likes to choice two same prime 
    numbers so, here i try to avoid this behavior'''

    @staticmethod
    def check_duplicates(*args) -> bool:

        checkDuplicatesSet: set = set(args)
        if len(checkDuplicatesSet) != len(args):
            return True
        return False

    '''For encrypt and decrypt with the values of the ASCII table its necessary to have a range 
    of all of the Unicode codes, in this case algorithm uses 255 chars limit '''

    '''If you need more Unicode characters, you can change the value above, not every browser has too many codes
       P * q < `value`  '''

    @staticmethod
    def check_all_ascii_codes(p: int, q: int) -> bool:

        if p * q < 1000:
            return True
        return False

    '''As in the name function, Euclid algorithm for cheking if 2 numbers are not factor '''

    @staticmethod
    def check_if_not_factor_euclid(e: int, n: int) -> int:
        while n != 0:
            e, n = n, e % n
        return e
