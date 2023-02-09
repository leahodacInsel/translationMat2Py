import tkinter as tk
from tkinter import filedialog
import pandas as pd

def get_files(mode):
    # Input: 'select' or 'test'. Test leads to a fixed list used for
    # testing, 'select' allows any input of excel sheet.

    # Output: path and cell of filenames
    if 'select' in mode:
        # Patients graph data(vol, flow)
        root = tk.Tk()
        root.withdraw()
        curve_file_names = filedialog.askopenfilenames(filetypes=[("text files", '*.txt')], title='Select curves data')

        # Patients graph data(vol, flow)
        root = tk.Tk()
        root.withdraw()
        vars_file_names = filedialog.askopenfilenames(filetypes=[("tables", '*.x*')], title='Select the patient data')

    elif 'test' in mode:
        vars_file_names = r'L:\KKM_LuFu\OfficeData\Biomedical Engineers\Lea\project QC\code_marion\'Patients_values'
        curve_file_names = r'L:\KKM_LuFu\OfficeData\Biomedical Engineers\Lea\project ' \
                          r'QC\code_marion\Rüegsegg_00093878_09062021_080000'

    if not curve_file_names or not vars_file_names:
        print('Error, no files selected, please retry')

    return curve_file_names[0], vars_file_names[0]


if __name__ == '__main__':

    # Select files and init params
    '''For this algorithm to work the excel files should be in english and all 
    should contain the 'best trial' as their first trial. 
    However in the results this 'best trial' will not appear'''

    curveFileNames, varsFileNames = get_files('select')
    print('Curve: ', curveFileNames, '\nVars: ', varsFileNames)

    fileNumber = len(curveFileNames)+len(varsFileNames)

    numerical_data = pd.read_table(varsFileNames)

    print(numerical_data)




