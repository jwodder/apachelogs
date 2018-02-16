import pytest
from   apachelogs import LogFormat, InvalidDirectiveError

@pytest.mark.parametrize('fmt', [
    '%',
    '% ',
    '%^x',
    '%^',
    '%{param',
])
def test_malformed_directive(fmt):
    with pytest.raises(ValueError):
        LogFormat(fmt)

@pytest.mark.parametrize('fmt', [
    '%x',
    '%^xx',
    '%{param}x',
    '%{x}a',
    '%{x}b',
    '%C',
])
def test_unknown_directive(fmt):
    with pytest.raises(InvalidDirectiveError) as excinfo:
        LogFormat(fmt)
    assert excinfo.value.directive == fmt
