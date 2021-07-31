import sys

def format_shape_pharm(lig):
    ligFile = open(lig, 'r')

    for line in ligFile:
        if 'HETATM' in line or 'ATOM' in line:
            resi = int(line.split( )[1])
            x = float(line.split( )[6])
            y = float(line.split( )[7])
            z = float(line.split( )[8])
            pharm_info = float(line.split( )[9])
            print("ATOM   {: >4d}  SHA SHA S{: >4d}     {: 7.3f} {: 7.3f} {: 7.3f} {:5.2f}  1.00 ".format(resi, resi, x, y, z, pharm_info))
    print("END")


def format_shape(lig):
    ligFile = open(lig, 'r')

    for line in ligFile:
        if 'HETATM' in line or 'ATOM' in line:
            resi = int(line.split( )[1])
            x = float(line.split( )[6])
            y = float(line.split( )[7])
            z = float(line.split( )[8])
            print("ATOM   {: >4d}  SHA SHA S{: >4d}     {: 7.3f} {: 7.3f} {: 7.3f}  1.00  1.00 ".format(resi, resi, x, y, z))
    print("END")
    
if __name__ == "__main__":
    mode = sys.argv[1]
    lig = sys.argv[2]

    if mode == "shape":
        format_shape(lig)

    if mode == "pharm":
        format_shape_pharm(lig)
        
