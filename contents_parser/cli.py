import click

from contents_parser.parse import Parser, ContentsStats, Architecture


@click.command()
@click.option("-a", "--arch", help="Architecture contents file to get", required=True)
def get_top_deb_packages_for_arch(arch: str):
    """ 
    Simplify the cli handling by using Click API
    """
    try:
        arch = Architecture[arch.upper()]
    except KeyError:
        print(
            f"KeyError: Incorrect argument passed for architecture \n"
            "Must be one of: \n"
            f"{[e.name.lower() for e in Architecture]}"
        )
        return
    contents_df = Parser.parse(arch)
    top_packages = ContentsStats.get_top_packages(contents_df)
    ContentsStats.print_top_n_packages(top_packages, 10)
