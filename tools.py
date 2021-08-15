def xyz_writer(array, filename = 'test'):
    """The array is a numpy array or a list of lists. We write it into a xyz file.
    filename is a string, which is the name of the xyz file being created.
    """
    with open("{}.xyz".format(filename), 'w') as f:
        for coordinates in array:
            f.write("{} {} {}\n".format(coordinates[0], coordinates[1], coordinates[2]))
    f.close() 
    
def xyz_parser(filename):
    text = open(filename, "r")

    atom_list = []
    for line in text:
        atom_list.append(list(map(float, line.split()[:3])))
    return np.array(atom_list)
   
def laplacian_parser(filename):
    """filename is the name of persistent laplacian"""
    text = open(filename, "r")

    matrices = []
    mat = []
    for line in text:
        if line.split() != ['END']:
            mat.append(list(map(float, line.split())))
        else:
            matrices.append(np.array(mat))
            mat = []
    return matrices
