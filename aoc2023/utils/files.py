from os import PathLike


def read_as_string(path: str | bytes | PathLike) -> str:
    with open(path) as f:
        return f.read()


def read_as_lines(path: str | bytes | PathLike) -> list[str]:
    return read_as_string(path).splitlines()
