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
        curve_file_names = filedialog.askopenfilenames(filetypes=[("text files", '*.xml')], title='Select XML curves data')

        # Patients graph data(vol, flow)
        root = tk.Tk()
        root.withdraw()
        vars_file_names = filedialog.askopenfilenames(filetypes=[("tables", '*.x*')], title='Select the patient data')
        return curve_file_names[0], vars_file_names[0]

    elif 'test' in mode:
        vars_file_names = r'L:\KKM_LuFu\OfficeData\Biomedical Engineers\Lea\03.Projects\project QC\code_marion\Patients_values.xlsx'
        curve_file_names = r'L:\KKM_LuFu\OfficeData\01. Documentation\SpiroQC\0012523879_ test julia.xml'
        return curve_file_names, vars_file_names

    if not curve_file_names or not vars_file_names:
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

    curveFileNames, varsFileNames = get_files('test')
    print('Curve: ', curveFileNames, '\nVars: ', varsFileNames)

    fileNumber = len(curveFileNames)

    numerical_data = pd.read_excel(Path(varsFileNames))
    print(numerical_data)

    # init results table
    results = init_res_table()
    print(results)

    # for file in curveFileNames:

        # init plot --> XML files


        # numerical algo







