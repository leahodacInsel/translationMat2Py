import tkinter as tk
from tkinter import filedialog
import pandas as pd
from pathlib import Path
import tables as tb
import numpy as np
from read_from_xml import get_raw_vectors, plot_raw_curves, get_parameters


def get_files(mode):
    # Input: 'select' or 'test'. Test leads to a fixed list used for
    # testing, 'select' allows any input of excel sheet.

    # Output: path and cell of filenames
    if 'select' in mode:
        # Patients graph data(vol, flow)
        root = tk.Tk()
        root.withdraw()
        file_names = filedialog.askopenfilenames(filetypes=[("text files", '*.xml')], title='Select XML curves data')


    elif 'test' in mode:
        file_names = r'L:\KKM_LuFu\OfficeData\01. Documentation\SpiroQC\0016504909_testLea.xml'
        return file_names

    if not file_names:
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

    FileNames = get_files('test')
    print('Curve: ', FileNames)

    fileNumber = len(FileNames)

    # init results table
    results = init_res_table()
    print(results)

    #for file[0][] in FileNames:
    data = get_parameters(FileNames)
    print(data)


        # init plot --> XML files


        # numerical algo







