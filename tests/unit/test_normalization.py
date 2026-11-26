import pytest

from web_autocomplete_service.core.normalization import normalize

@pytest.mark.parametrize("raw, expected", [
    ("CRYPT", "crypt"),
    ("Crypt", "crypt"),
    ("  crypt  ", "crypt"),
    ("crypto   graphic", "crypto graphic"),         
    ("  Café  sans   crème ", "café sans crème"),
    ("cryptographic algorithm", "cryptographic algorithm"),
])
def test_normalize(raw, expected):
    assert normalize(raw) == expected