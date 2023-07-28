import gzip
import pandas as pd
import shutil
from pathlib import Path
from urllib.request import urlopen
from enum import Enum
from urllib.parse import urlparse, urljoin

# Enumeration of possible architectures
# This is just to make it clearer about what options are available and easier to
# know if an incorrect option was passed
Architecture = Enum(
    'Architecture', ["AMD64", "ARM64", "ARMEL", "ARMHF",
                     "I386", "MIPS64EL", "MIPSEL", "PPC64EL", "S390X"]
)

# Data frame keys for table made from contents file
D_FILENAME = "filename"
D_PACKAGE = "package"

# Other stray constants for decoding
K_UTF8 = "utf-8"


class Parser:
    """ 
    Utility class to do the downloading and parsing of the contents file 
    """
    # Some contents only the parser should know about
    _K_MIRROR_LINK = urlparse(
        "http://ftp.uk.debian.org/debian/dists/stable/main/")
    _K_CONTENTS_FILE_PATTERN = "Contents-*.gz"
    _K_DOWNLOADS_FOLDER = Path("../downloads")

    @classmethod
    def parse(cls, chosen_arch: Architecture) -> pd.DataFrame:
        # Download file -> get file path to downloaded file -> parse into df
        uncompressed = cls._download_file_contents(chosen_arch)
        return cls._process_uncompressed_file_to_df(uncompressed)

    @classmethod
    def _download_file_contents(cls, chosen_arch: Architecture) -> Path:
        # The contents files all follow the pattern of
        # Contents-{architecture}.gz where {architecture} is always in lowercase
        # Generate the string that is added to the end of the constant URL
        # to know which file to download
        chosen_arch_string = str(chosen_arch.name).lower()
        chosen_contents_file = cls._K_CONTENTS_FILE_PATTERN.replace(
            "*", chosen_arch_string)
        contents_file_url = urljoin(
            cls._K_MIRROR_LINK.geturl(), chosen_contents_file)

        # Simply request then download to folder relative to this file
        # Can be accomplished without downloading and just passing the filehandle around
        # Didn't see much performance difference so stuck with this method as can
        # rerun later parts without having to perform the download
        response = urlopen(contents_file_url)
        download_folderpath = Path(__file__).parent / cls._K_DOWNLOADS_FOLDER
        download_folderpath.mkdir(exist_ok=True, parents=True)
        copied_contents_filepath = download_folderpath / chosen_contents_file
        print(
            f"Downloading file from {contents_file_url} -> {copied_contents_filepath}")
        with open(copied_contents_filepath, "wb") as f:
            shutil.copyfileobj(response, f)
        return copied_contents_filepath

    @classmethod
    def _process_uncompressed_file_to_df(cls, uncompressed: Path) -> pd.DataFrame:
        # Simply read line by line
        # List of dictionaries which are then agregated into a dataframe
        print("Processing Contents gzip to dataframe")
        uncompressed = gzip.GzipFile(uncompressed)
        rows = []
        for line in uncompressed:
            # Tables are broken up into
            # FILENAME     PACKAGE
            # split based on this pattern
            associated_file, _, package = line.decode(
                K_UTF8).rpartition(" ")
            associated_file = associated_file.strip()
            package = package.strip()
            row_dict = {
                D_FILENAME: associated_file,
                D_PACKAGE: package
            }
            rows.append(row_dict)

        parsed_data = pd.DataFrame(
            rows
        )
        return parsed_data


class ContentsStats:
    """ 
    Utility class to calculate the statistics on the contents data frame 
    """
    @classmethod
    def get_top_packages(cls, contents_df: pd.DataFrame) -> pd.Series:
        # Value counts does all the hard work for me of finding the
        # amount of times the package name repeats in the dataframe
        # and is much much quicker then iterating through the df myself
        return contents_df[D_PACKAGE].value_counts()

    @classmethod
    def print_top_n_packages(cls, top_packages: pd.Series, n: int):
        # Pretty print top packages
        print("Rank  Package  Num Files")
        for rank, package_name, num_files in zip(
                range(1, n + 1),
                top_packages.index,
                top_packages.to_numpy()[0:n]):
            # Just to make it look nicer, clip the packages extra path variables and
            # only print name
            clipped_package_name = package_name.split('/')[-1]
            print(f"{rank}: {clipped_package_name} -- {num_files}")


if __name__ == "__main__":
    # DEBUG tests
    chosen_arch = Architecture.I386
    contents_df = Parser.parse(chosen_arch)
    top_packages = ContentsStats.get_top_packages(contents_df)
    ContentsStats.print_top_packages(top_packages)
