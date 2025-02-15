""" xyz
Parser of the .xyz file format. 
"""
from dataclasses import dataclass
from typing import Iterator


class ParseError(Exception):
    """ Error in parsing an xyz file. """


@dataclass
class MoleculeXYZ:
    natoms: int
    comment: str
    data: list


def parse_molecule(xyz_file: Iterator[str], natoms_line: str) -> MoleculeXYZ:
    try:
        natoms = int(natoms_line)
    except ValueError:
        raise ParseError(f"Expected number of atoms. Got {natoms_line}") from None

    comment = next(xyz_file).strip()
    data = list()
    for _ in range(natoms):
        try:
            line = next(xyz_file)
        except StopIteration:
            raise ParseError(f"Expected to find {natoms} atoms. Found only {len(data)}")
        atom_line = line.split()
        if len(atom_line) >= 4:
            atom = {
                    "atom": atom_line[0],
                    "xyz": [float(coord) for coord in atom_line[1:4]],
                    "extra": [float(coord) for coord in atom_line[4:]],
            }
            data += [atom]
        else:
            raise RuntimeError(
                "XYZ requires at least an atom symbol and three coordinates. "
                "Got:\n"
                f"{line}"
            )

    entry_lengths = set(len(atom) for atom in data)
    if len(entry_lengths) != 1:
        raise ParseError("Varying input length.")

    return MoleculeXYZ(natoms=natoms, comment=comment, data=data)


def parse(xyz_file: Iterator[str]) -> list[MoleculeXYZ]:
    """ Use this function to parse an xyz file.
    See the example below for a sample use.

    Water::
        >>> xyz_file=iter('''3
        ... water
        ... H 0.0 -1.0 0.0
        ... O 0.0  0.0 1.0
        ... H 0.0  1.0 0.0'''.split('\\n'))
        >>> parsed_xyz = parse(xyz_file)
        >>> water = parsed_xyz[0]
        >>> water.natoms
        3
        >>> water.comment
        'water'
        >>> atoms = water.data
        >>> atoms[0]['atom']
        'H'
        >>> atoms[0]['xyz']
        [0.0, -1.0, 0.0]
    """
    molecules = list()
    while True:
        try:
            natoms_line = next(xyz_file)
        except StopIteration:
            break
        molecules += [parse_molecule(xyz_file, natoms_line)]
    return molecules
