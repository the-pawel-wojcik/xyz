# xyz_parser
A python parser for the fileformat (.xyz) used for storing computational
chemistry data.

# Install
```bash
pip install xyz_parser
```

# Use
```python
import xyz_parser

with open('molecules.xyz') as mols_file:
    molecule = xyz_parser.parse(mols_file)

for molecule in molecules:
    print(f'{molecule.natoms=}')
    print(f'{molecule.comment=}')
    for atom in molecule.data:
        print(f'{atom['atom']=}', end='')
        print(f'{atom['xyz']=}', end='')
        print(f'{atom['extra']=}')
```
