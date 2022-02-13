import os
import numpy as np
import sys

# run this in bertini_related folder
filename = sys.argv[1]

#
filtration_list = np.arange(60, 250, 1) # indeed radius, only serve as label
#filtration_list = [0.5]

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

def expr(array, style):
    """input: np 1d array
    """
    result = ''
    d = array.size - 1
    if style == 'python':
        for i in range(d):
            if array[i] == 0.0:
                continue
            if array[i+1] >= 0.0:
                result += '{}*x**{}+'.format(str(array[i]) ,str(d-i))
            else:
                result += '{}*x**{}'.format(str(array[i]) ,str(d-i))
    if style == 'julia':
        for i in range(d):
            if array[i] == 0.0:
                continue
            if array[i+1] >= 0:
                result += '{}*x^{}+'.format(str(array[i]) ,str(d-i))
            else:
                result += '{}*x^{}'.format(str(array[i]) ,str(d-i))  
    if array[-1] != 0.0:
        result += str(array[-1])
    if result[-1] == '+':
        result = result[:-1]
    return result

def mkdir_p(dir):
    """make a directory (dir) if it doesn't exist"""
    if not os.path.exists(dir):
        os.mkdir(dir)


    

# store job file
file_directory = "{}/{}".format(os.getcwd(), filename)
mkdir_p(file_directory)
output_directory = "{}/output_{}".format(os.getcwd(), filename)
mkdir_p(output_directory)

matrices = laplacian_parser("{}/persistent_laplacian.txt".format(file_directory))

# loop start here
for ind, i in enumerate(filtration_list):
#i = 2
#if i == 2:

    for j in range(3):
        poly_directory = "{}/fil={}_dim={}".format(file_directory, str(i), str(j))
        mkdir_p(poly_directory)
        if matrices[ind*3+j].size == 0:
            output_file = os.path.join(output_directory, "output_{}_fil={}_dim={}.txt".format(filename, str(i), str(j)))
            with open(output_file, "w+") as f:
                f.writelines("the matrix don't exist and hence no corresponding polynomial.\n")
            continue
        polynomial = expr(np.poly(matrices[ind*3+j])/np.amax(np.poly(matrices[ind*3+j])), style = 'julia')
        input_file = os.path.join(poly_directory, "input_fil={}_dim={}".format(str(i), str(j)))

        with open(input_file, 'w+') as fh:
            fh.writelines("CONFIG\n")
            fh.writelines("MPTYPE: 2;\n")
            #fh.writelines("FINALTOL: 1e-8;\n")
            fh.writelines("COEFFBOUND: 100;\n")
            fh.writelines("DEGREEBOUND: 80;\n")
            fh.writelines("AMPSAFETYDIGITS1: 1;\n")
            fh.writelines("AMPSAFETYDIGITS2: 1;\n")
            fh.writelines("AMPMAXPREC: 3328;\n")
            fh.writelines("END;\n")
            fh.writelines("INPUT\n")
            fh.writelines("function f;\n")
            fh.writelines("variable_group x;\n")
            fh.writelines("f = {};\n".format(polynomial))
            fh.writelines("END;\n")


        job_file = os.path.join(file_directory, "{}_fil={}_dim={}.job".format(filename, str(i), str(j)))

        with open(job_file, 'w+') as fh:
            fh.writelines("#!/bin/bash --login\n")
            fh.writelines("#SBATCH --nodes=1\n")
            fh.writelines("#SBATCH --ntasks-per-node=1\n")
            fh.writelines("#SBATCH --time=0:30:00\n")
            fh.writelines("#SBATCH --mem=16gb\n")
            fh.writelines("#SBATCH --output=./output_{}/output_{}_fil={}_dim={}.txt\n".format(filename, filename, str(i), str(j)))
            fh.writelines("cd\n")
            fh.writelines("cd {}\n".format(poly_directory))
            fh.writelines("./../../../Bertini/bertini {}\n".format(input_file))
        #fh.writelines("scontrol show jobid -dd $SLURM_JOBID\n")

        os.system("sbatch {}".format(job_file))
    
# end of loop





            