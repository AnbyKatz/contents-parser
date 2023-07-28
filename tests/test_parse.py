import pytest
from contents_parser.parse import Parser, Architecture


@pytest.mark.parametrize("arch", ["AMD64", "ARM64", "ARMEL", "ARMHF", "I386", "MIPS64EL", "MIPSEL", "PPC64EL", "S390X"])
def test_parser(arch: Architecture):
    try:
        arch = Architecture[arch]
        Parser.parse(arch)
    except RuntimeError as e:
        pytest.fail(f"Failed to parse the contents file {e}")
