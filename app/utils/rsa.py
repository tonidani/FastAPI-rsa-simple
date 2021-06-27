#RSA Encryption using python
import random
from typing import Tuple
from .number_utils import NumberUtils

class Rsa():

    def __init__(self):

        primesList = [i for i in range(0, 100) if NumberUtils.is_prime(i)] # append only prime numbers
        self._p, self._q = self.__get_prime_numbers(primesList)
        self._n = self._p * self._q
        self._phi = (self._p-1) * (self._q-1)
        self._e = self.__get_exponent(self._phi)
        self._public_key, self._private_key = self.__generate_key_pairs(self._e, self._n, self._phi)


    def __repr__(self) -> dict:
        return str(self.__dict__)


    '''Getters'''

    @property
    def p(self) -> int:
        return self._p
    
    @property
    def q(self) -> int:
        return self._q
    
    @property
    def n(self) -> int:
        return self._n
    
    @property
    def phi(self) -> int:
        return self._phi
    
    @property
    def e(self) -> int:
        return self._e

    @property
    def public_key(self) -> dict:
        return self._public_key

    @property
    def private_key(self) -> dict:
        return self._private_key

    
    '''This function allows choose two numbers p and q such that they cover 
    the entire ascii table and are not equals - this could cause problems in the algorithm'''


    def __get_prime_numbers(self, primesList: int) -> Tuple[int, int]:
        
        noDuplicates = True
        allAsciiCodes = True
        while noDuplicates or allAsciiCodes:
            p: int = random.choice(primesList)
            q: int = random.choice(primesList)
            noDuplicates = NumberUtils.check_duplicates(p, q)
            allAsciiCodes = NumberUtils.check_all_ascii_codes(p, q)

        return p, q    

    ''' This function chooses a exponent: the rule is 1 < e < phi | and e should not be a factor of phi '''

    def __get_exponent(self, phi: int) -> int:
        
        e: int
        for i in range(2, phi):
                if NumberUtils.check_if_not_factor_euclid(i, phi) == 1:
                    e=i
                    return e
 
    ''' This function generates Dicts with key pairs of public and priv keys '''
    
    def __generate_key_pairs(self, e: int, n: int, phi: int) -> Tuple[dict, dict]:

        public_key: dict = {"key" : e, "n": n}
        private_key: dict = {"key": 0, "n": n}
        x: int = -1
        while x != 0:
            private_key["key"] += 1
            x = (public_key["key"] * private_key["key"] - 1 ) % phi
        
        return public_key, private_key

    
    ''' Here uses algebra for encrypt the message with the Unicode representation of characters in ascii table '''
    # c = (letters to int) ^ e % n

    def encrypt_RSA(self, message: str, public_key: int) -> str:

        message = [ord(i) for i in message]
        encryptedMessage = ''.join([chr(i ** public_key["key"] % public_key["n"]) for i in message])

        return encryptedMessage

    ''' Same as above, but in reverse '''
    # c ^ e % n

    def decrypt_RSA(self, encryptedMessage: str, private_key: int) -> str:

        encryptedMessage = [ord(i) for i in encryptedMessage]
        decryptedMessage =''.join([chr(i ** private_key["key"] % private_key["n"] ) for i in encryptedMessage])

        return decryptedMessage
 
if __name__ == "__main__":
    rsa = Rsa()