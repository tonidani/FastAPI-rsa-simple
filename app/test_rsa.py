from rsa import Rsa
import pytest

class TestRsa:

    @pytest.fixture
    def rsa(self):
        rsa = Rsa()
        return rsa

    @pytest.fixture
    def message(self):
        return 'Some message to encrypt with special chars !@$63^& \n \t'

    def test_create_rsa(self):
        rsa = Rsa()

        assert isinstance(rsa, Rsa)

    def test_p_q_not_equal(self, rsa):

        assert rsa.p != rsa.q

    def test_e_is_between_one_n(self, rsa):

        assert rsa.n > rsa.e > 1

    def test_key_pairs_diff(self, rsa):

        assert rsa.public_key != rsa.private_key

    def test_message_not_equal_encrypted(self, message, rsa):

        assert message != rsa.encrypt_RSA(message, rsa.public_key)

    def test_message_equal_decrypted(self, message, rsa):

        encrypted = rsa.encrypt_RSA(message, rsa.public_key)

        assert message == rsa.decrypt_RSA(encrypted, rsa.private_key)