import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pandas as pd


def get_files(mode):
    # Input: 'select' or 'test'
    # Output: paths and filenames

    if 'select' in mode:
        # Patients graph data(vol, flow)
        root = tk.Tk()
        root.withdraw()
        file_names = filedialog.askopenfilenames(filetypes=[("text files", '*.xml')], title='Select XML curves data')

        paths = ["" for x in range(len(file_names))]
        nameFiles = ["" for x in range(len(file_names))]

        for nFile, file in enumerate(file_names):
            x = file_names[nFile].rfind("/")
            paths[nFile] = file_names[nFile][:x]
            nameFiles[nFile] = file_names[nFile][x + 1:]

    elif 'test' in mode:
        paths = list([r'\\filer300\USERS3007\I0337516\Desktop'])
        nameFiles = list(['0011972203.xml'])

    if not nameFiles:
        print('Error, no files selected, please retry')
        return

    return paths, nameFiles


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
