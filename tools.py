def mkdir_p(dir):
    """make a directory (dir) if it doesn't exist"""
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
        
def array_writer(array, filename = 'test.txt'):
    """
    The array is a numpy array or list of lists. 
    We write it into a file.
    filename is the name of the output file.
    """
    array = np.array(array)
    with open(filename, 'w') as f:
        for i, row in enumerate(array):
            for item in row:
                f.write("{} ".format(item))
            if i != (array.shape[0]-1): # make sure that the last line is not empty.
                f.write("\n")
    f.close() 
    
def matrix_reader(filename = 'test.txt'):
    text = open(filename, "r")
    array_list = []
    for line in text:
        array_list.append(list(map(float, line.split())))
    text.close()
    return np.array(array_list)  

def array_parser(filename = 'test.txt'):
    """
    Return a list of lists.
    """
    res = []
    with open(filename, 'r') as f:
        for line in f:
            res.append(list(map(float, line.split())))
    f.close()
    return res
    
def xyz_parser(filename):
    text = open(filename, "r")

    atom_list = []
    for line in text:
        atom_list.append(list(map(float, line.split()[:3])))
    text.close()
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
    text.close()
    return matrices

def pqr_parser(filename):
    import numpy as np
    f = open(filename, 'r')
    coordinates = []
    charges = []
    for line in f:
        if len(line.split()) == 10:
            coordinates.append(list(map(float, line.split()[-5:-2])))
            charges.append(float(line.split()[-2]))
    return np.array(coordinates), np.array(charges)
