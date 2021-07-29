import sys

def format_shape(lig):
    ligFile = open(lig, 'r')
    outputFile = open('shape_pharm.pdb', 'w')

    for line in ligFile:
        resi = int(line.split( )[1])
        x = float(line.split( )[6])
        y = float(line.split( )[7])
        z = float(line.split( )[8])
        pharm_info = float(line.split( )[9])
        outputFile.write("ATOM    {: >3d}  SHA SHA S {: >3d}     {: 7.3f} {: 7.3f} {: 7.3f} {:5.2f}  0.00 \n".format(resi, resi, x, y, z, pharm_info))

    outputFile.close()
    
if __name__ == "__main__":
    lig = sys.argv[1]
    format_shape(lig)
