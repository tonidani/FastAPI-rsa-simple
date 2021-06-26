
class NumberUtils():
    
    '''This functions works with the list comprehesion and catches only the prime numbers'''
    
    @staticmethod
    def is_prime(number: int) -> bool:
        
        if number > 1:
            for i in range(2, int(number/2)+1):
                if (number % i) == 0:
                    return False
            return True
        return False

    '''I need this function because the "random" module in rsa2 file somethimes likes to choice two same prime 
    numbers so, here i try to avoid this behavior'''

    @staticmethod
    def check_duplicates(*args) -> bool:
        
        checkDuplicatesSet: set =  set(args)
        if len(checkDuplicatesSet) != len(args):
            return True
        return False

    '''For encrypt and decrypt with the values of the ASCII table I need to have a range 
    of all of the int codes, in this case I put 255 chars limit '''


    @staticmethod
    def check_all_ascii_codes(p: int, q: int) -> bool:
        
        if p * q < 255:
            return True
        return False

    
    '''As in the name function, Euclid algorithm for cheking if 2 numbers are not factor '''

    @staticmethod
    def check_if_not_factor_euclid(e: int, n: int) -> int:
        while n != 0:
            e, n = n, e % n
        return e