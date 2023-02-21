import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pathlib import Path
import tables as tb
import numpy as np
from read_from_xml import get_raw_vectors, plot_raw_curves, get_parameters
from numerical_algo import flowchart
from initializations import separate_inspi_expi


def get_files(mode):
    # Input: 'select' or 'test'. Test leads to a fixed list used for
    # testing, 'select' allows any input of excel sheet.

    # Output: path and cell of filenames
    if 'select' in mode:
        # Patients graph data(vol, flow)
        root = tk.Tk()
        root.withdraw()
        file_names = filedialog.askopenfilenames(filetypes=[("text files", '*.xml')], title='Select XML curves data')
        '''TROUVER COMMENT SEPARER NOM FICHIER ET CHEMIN !!!'''

    elif 'test' in mode:
        path = r'L:\KKM_LuFu\OfficeData\01. Documentation\SpiroQC\04. SentrySuite export'
        nameFile = '0016504909_test200223'
        return path, nameFile

    if not nameFile:
        print('Error, no files selected, please retry')


def init_res_table():

    # This function build the results table which will be saved as an excel later.
    dtypes = np.dtype(
        [
            ('PatientID', str),
            ('ID_curve', str),
            ('Date', str),
            ('test_grade', str),
            ('Trials', float),
            ('best_FEV1', float),
            ('best_FVC', float),
            ('numerical_QC_accepted', float),
            ('numerical_criteria', float),
            ('graphical_criteria', float),
            ('perfect_quality_curve', float),
            ('average_quality_curve', float),
            ('poor_quality_curve', float),
            ('Age criteria', float),
            ('Start of test criteria', float),
            ('Start of test VBE FVC criteria', float),
            ('Start of test VBE 0.1 criteria', float),
            ('Start of test FETPEF criteria', float),
            ('Start of test dPEF 10 criteria', float),
            ('Start of test dPEF -10 criteria', float),
            ('Start of the test Hesitation time criteria', float),
            ('Max inspiration criteria', float),
            ('Max inspiration FVCIN FVC criteria', float),
            ('Max inspiration FVCIN FVC < 0.05 FVC criteria', float),
            ('End of test criteria', float),
            ('End of test EOTV criteria', float),
            ('End of test FET criteria', float),
            ('End of test dFVC criteria', float),
            ('End of test delta dFVC criteria', float),
            ('Repeatability criteria', float),
            ('Repeatability Tex criteria', float),
            ('Repeatability dFEV1 criteria', float),
            ('Repeatability delta dFEV1 criteria', float),
            ('Repeatability dFEV 0.75 criteria', float),
            ('Repeatability delta dFEV 0.75 criteria', float),
            ('Repeatability dFVC criteria', float),
            ('Repeatability delta dFVC criteria', float),
            ('peak_criteria', float),
            ('peak_concavity_score', float),
            ('cough_criteria', float),
            ('obstructive_criteria', float),
            ('irregular_criteria', float),
            ('suboptimal_criteria', float),
            ('beta_angle', float),
            ('leak_criteria', float),
            ('glottic_criteria', float)
        ]
    )

    df = pd.DataFrame(np.empty(0, dtype=dtypes))

    return df


if __name__ == '__main__':
    # Select files and init params
    '''For this algorithm to work the excel files should be in english and all 
    should contain the 'best trial' as their first trial. 
    However in the results this 'best trial' will not appear'''

    path, nameFile = get_files('test')

    fileNumber = len(nameFile)

    # init results table
    results = init_res_table()
    #print(results)

    # for file[0][] in FileNames:
    data = get_parameters(path, nameFile)
    vol_VT, time_VT, flow_FV, vol_FV = get_raw_vectors(path, nameFile)

    # curves are not separated by trials, vol_VT is composed of the curves of each trial
    data['vol_VT'] = vol_VT
    data['time_VT'] = time_VT
    data['flow_FV'] = flow_FV
    data['vol_FV'] = vol_FV

    plot_raw_curves(vol_VT, time_VT, flow_FV, vol_FV, 'testFile')


    data = computedFEV75(data)
    data = computedPEF(data)

    trialNum = len(vol_VT)
    for n in range(trialNum):
        trialName = "trial" + str(n)
        criteria = flowchart(data[trialName])
        # inspis, expis = separate_inspi_expi(data)

    print('\n\n...jusqu\'ici tout va bien')




