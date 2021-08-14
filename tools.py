def xyz_writer(array, filename = 'test'):
    """The array is a numpy array or a list of lists. We write it into a xyz file.
    filename is a string, which is the name of the xyz file being created.
    """
    with open("{}.xyz".format(filename), 'w') as f:
        for coordinates in array:
            f.write("{} {} {}\n".format(coordinates[0], coordinates[1], coordinates[2]))
    f.close() 
