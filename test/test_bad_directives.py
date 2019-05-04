import pytest
from   apachelogs import LogFormat, InvalidDirectiveError, UnknownDirectiveError

@pytest.mark.parametrize('fmt', [
    '%',
    '% ',
    '%^x',
    '%^',
    '%{param',
])
def test_malformed_directive(fmt):
    with pytest.raises(InvalidDirectiveError) as excinfo:
        LogFormat(fmt)
    assert str(excinfo.value) \
        == 'Invalid log format directive at column 0 of {!r}'.format(fmt)
    assert excinfo.value.pos == 0
    assert excinfo.value.log_format == fmt

@pytest.mark.parametrize('fmt', [
    '%x',
    '%^xx',
    '%{param}x',
    '%{x}a',
    '%{x}b',
    '%C',
])
def test_unknown_directive(fmt):
    with pytest.raises(UnknownDirectiveError) as excinfo:
        LogFormat(fmt)
    assert str(excinfo.value) \
        == 'Unknown log format directive: {!r}'.format(fmt)
    assert excinfo.value.directive == fmt
