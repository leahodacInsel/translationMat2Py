from read_from_xml import get_raw_vectors, plot_raw_curves, get_parameters
from numerical_algo import flowchart
from initializations import get_files, init_res_table



if __name__ == '__main__':
    # Select files and init params
    paths, nameFiles = get_files('test')

    # init results table
    results = init_res_table()

    data = dict()

    for idx, nameFile in enumerate(nameFiles):
        data[nameFile] = dict()

        data[nameFile] = get_parameters(data[nameFile], paths[idx], nameFile)
        data[nameFile] = get_raw_vectors(data[nameFile], paths[idx], nameFile)
        plot_raw_curves(data[nameFile], nameFile)

        criteria = flowchart(data[nameFile])



print('\n\n...jusqu\'ici tout va bien')





'''
To do:

- Output index of the best trial

- print code message of the software

- Remove space around key names in parameter dictionary

- change dFEV75 and dPEF --> difference between the two best curves

- check dFEV1 same ?

- change FVC for FEV1/FEV1%FVC * 100

'''


