import sys

# slice objects for the different PDB v3 columns
atom_record = slice(0, 6)
atom_serial = slice(6, 11)
atom_name = slice(12, 16)
atom_altLoc = slice(16, 17)
atom_resName = slice(17, 20)
atom_chainID = slice(21, 22)
atom_resSeq = slice(22, 26)
atom_iCode = slice(26, 27)
atom_x = slice(30, 38)
atom_y = slice(38, 46)
atom_z = slice(46, 54)
atom_occ = slice(54, 60)
atom_temp = slice(60, 66)
atom_segid = slice(72, 76)
atom_element = slice(76, 78)
atom_model = slice(78, 80)


def format_shape_pharm(lig):
    ligFile = open(lig, 'r')

    atom_lines = (l for l in ligFile if l.startswith(("HETATM", "ATOM")))
    for line in atom_lines:
        resi = int(line[atom_serial])
        x = float(line[atom_x])
        y = float(line[atom_y])
        z = float(line[atom_z])
        pharm_info = float(line[atom_temp])
        print("ATOM   {: >4d}  SHA SHA S{: >4d}     {: 7.3f} {: 7.3f} {: 7.3f} {:5.2f}  1.00 ".format(resi, resi, x, y, z, pharm_info))
    print("END")
    ligFile.close()


def format_shape(lig):
    ligFile = open(lig, 'r')

    atom_lines = (l for l in ligFile if l.startswith(("HETATM", "ATOM")))
    for line in atom_lines:
        resi = int(line[atom_serial])
        x = float(line[atom_x])
        y = float(line[atom_y])
        z = float(line[atom_z])
        print("ATOM   {: >4d}  SHA SHA S{: >4d}     {: 7.3f} {: 7.3f} {: 7.3f}  1.00  1.00 ".format(resi, resi, x, y, z))
    print("END")
    ligFile.close()


if __name__ == "__main__":

    mode = sys.argv[1]
    lig = sys.argv[2]

    if mode == "shape":
        format_shape(lig)

    if mode == "pharm":
        format_shape_pharm(lig)
