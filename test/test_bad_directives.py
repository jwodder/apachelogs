import pytest
from   apachelogs import InvalidDirectiveError, LogParser, UnknownDirectiveError

@pytest.mark.parametrize('fmt', [
    '%',
    '% ',
    '%^x',
    '%^',
    '%{param',
])
def test_malformed_directive(fmt):
    with pytest.raises(InvalidDirectiveError) as excinfo:
        LogParser(fmt)
    assert str(excinfo.value) \
        == 'Invalid log format directive at index 0 of {!r}'.format(fmt)
    assert excinfo.value.pos == 0
    assert excinfo.value.format == fmt

@pytest.mark.parametrize('fmt', [
    '%x',
    '%^xx',
    '%{param}z',
    '%{x}a',
    '%{x}b',
    '%{%{x}a',
    '%C',
])
def test_unknown_directive(fmt):
    with pytest.raises(UnknownDirectiveError) as excinfo:
        LogParser(fmt)
    assert str(excinfo.value) \
        == 'Unknown log format directive: {!r}'.format(fmt)
    assert excinfo.value.directive == fmt

@pytest.mark.parametrize('fmt', [
    '%',
    '% ',
    '%^x',
    '%^',
    '%{param',
    #'%{x}a',  # actually parsed as an unknown directive
    '%<a',
    '%200a',
    '%!a'
    '%!200a',
])
def test_malformed_time_directive(fmt):
    with pytest.raises(InvalidDirectiveError) as excinfo:
        LogParser('%{' + fmt + '}t')
    assert str(excinfo.value) \
        == 'Invalid log format directive at index 0 of {!r}'.format(fmt)
    assert excinfo.value.pos == 0
    assert excinfo.value.format == fmt
