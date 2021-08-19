def matrix_writer(array, filename = 'test'):
    """array is a numpy array or list of lists. We write it into a txt file.
    filename is the name of the txt file.
    """
    with open("{}.txt".format(filename), 'w') as f:
        for row in array:
            for i, entry in enumerate(row):
                f.write("{} ".format(entry))
            f.write("\n")
    f.close() 
    
def matrix_reader(filename = 'test.txt'):
    text = open(filename, "r")
    array_list = []
    for line in text:
        array_list.append(list(map(float, line.split())))
    return np.array(array_list) 
    
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
