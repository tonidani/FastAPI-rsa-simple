from ..utils.number_utils import NumberUtils

class TestNumberUtils:
    def test_is_prime(self):
        assert NumberUtils.is_prime(5)
        assert not NumberUtils.is_prime(6)

    def test_check_duplicates(self):
        assert NumberUtils.check_duplicates(2, 2)
        assert not NumberUtils.check_duplicates(2, 5)

    def test_check_all_ascii_codes(self):
        assert NumberUtils.check_all_ascii_codes(2, 5)
        assert not NumberUtils.check_all_ascii_codes(2, 1000)

    def test_check_if_not_factor_euclid(self):
        assert NumberUtils.check_if_not_factor_euclid(2, 5)
        assert NumberUtils.check_if_not_factor_euclid(10, 5)