from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks
import numpy as np


def flowchart(data):

    compute_dFEV75man(data)
    compute_dPEFman(data)
    compute_dFEV1man(data)
    compute_dFVCman(data)
    compute_tex(data)

    # check if dataTrial contain needed info
    keys_needed = {'TestDate', 'BirthDate', 'VBE%FVC', 'VBEex ', 'FETPEF', 'dPEF%_man', 'Tdel', 'FVC IN', 'FVC   ', 'EOTV',
                   'FET   ', 'dFVC_man', 'dFVC%_man', 'tex', 'dFEV1_man',  'dFEV1%_man', 'dFEV75_man', 'dFEV75%_man'}
    for key in keys_needed:
        if key not in data.keys():
            print(key, ' is not in dataTrial')

    criterias = dict()

    # Start of test

    for nTrial in range(len(data['FETPEF'])):

        criteria = dict()
        age = ((datetime.strptime(data['TestDate'], '%Y-%m-%d')) - (
            datetime.strptime(data['BirthDate'], '%Y-%m-%d')))
        criteria['age'] = age.days / 365.25

        # BEV < 5% FVC or < 0.1L
        if data['VBE%FVC'][nTrial] < 5:
            criteria['start_VBE_FVC_crit'] = 1

        elif data['VBEex '][nTrial] < 0.1: # check that VBEex is BEV
            criteria['start_VBE_0_1_crit'] = 1
            criteria['start_VBE_FVC_crit'] = 0
        else:
            criteria['start_VBE_0_1_crit'] = 0
            criteria['start_VBE_FVC_crit'] = 0
            criteria['start_of_test_crit'] = 0
            criteria['accept'] = 0

        # FETPEF
        if float(data['FETPEF'][nTrial]) <= 150:
            criteria['start_FETPEF_crit'] = 1
        else:
            criteria['start_FETPEF_crit'] = 0
            criteria['start_of_test_crit'] = 0
            criteria['accept'] = 0

        # Delta PEF

        if data['dPEF%_man'] <= 10:
            criteria['start_dPEF_10_crit'] = 1
        elif data['dPEF%_man'] >= -10:
            criteria['start_dPEF_minus_10_crit'] = 1
            criteria['start_dPEF_10_crit'] = 0
        else:
            criteria['start_dPEF_minus_10_crit'] = 0
            criteria['start_dPEF_10_crit'] = 0
            criteria['start_of_test_crit'] = 0
            criteria['accept'] = 0


# this part doesn't appear in the mindmap

        # Hesitation time
        if 'Tdel' in data:
            if data['Tdel'][nTrial] <= 2:
                criteria['start_Tdel_crit'] = 1
                if 'start_of_test_crit' not in criteria:
                    criteria['start_of_test_crit'] = 1
            else:
                criteria['start_Tdel_crit'] = 0
                criteria['start_of_test_crit'] = 0
                criteria['accept'] = 0

        else:
            if criteria['start_dPEF_10_crit'] or criteria['start_dPEF_minus_10_crit']:
                criteria['start_of_test_crit'] = 1
            else:
                criteria['start_of_test_crit'] = 0



        # Max inspiration

        # FIVC - FVC <= 0.1 or <= 5% of FVC
        if data['FVC IN'][nTrial] - data['FVC   '][nTrial] <= 0.1: # check that FVC IN is FIVC
            criteria['max_insp_FVCIN_FVC_0_1_crit'] = 1
            criteria['max_insp_crit'] = 1
        elif data['FVC IN'][nTrial] - data['FVC   '][nTrial] <= 0.05 * data['FVC   '][nTrial]:
            criteria['max_insp_FVCIN_FVC_0_1_crit'] = 0
            criteria['max_insp_FVCIN_FVC_0_0_5_FVC_crit'] = 1
            criteria['max_insp_crit'] = 1
        else:
            criteria['max_insp_FVCIN_FVC_0_1_crit'] = 0
            criteria['max_insp_FVCIN_FVC_0_0_5_FVC_crit'] = 0
            criteria['max_insp_crit'] = 0
            criteria['accept'] = 0

        # Now split by age because it has some differences in criteria
        if float(criteria['age']) <= 6:
            criteria['age_crit'] = 1

            # End of forced expiration
            # volume_change < 0.025 & & volume_change_time >= 1 --> EOTV

            if data['EOTV'][nTrial] < 0.025: # check if EOTV is vol.change in 1s
                criteria['end_EOTV_crit'] = 1
                criteria['EOFE_crit'] = 1

            elif data[ 'FET   '][nTrial] >= 15:
                criteria['end_EOTV_crit'] = 0
                criteria['end_FET_crit'] = 1
                criteria['EOFE_crit'] = 1

            elif data['dFVC%_man'] <= 10:
                criteria['end_EOTV_crit'] = 0
                criteria['end_FET_crit'] = 0
                criteria['end_dFVC_delta_crit'] = 1
                criteria['EOFE_crit'] = 1

            elif data['dFVC%_man'] <= 0.1:
                criteria['end_EOTV_crit'] = 0
                criteria['end_FET_crit'] = 0
                criteria['end_dFVC_delta_crit'] = 0
                criteria['end_dFVC_crit'] = 1
                criteria['EOFE_crit'] = 1

            else:
                criteria['end_EOTV_crit'] = 0
                criteria['end_FET_crit'] = 0
                criteria['end_dFVC_delta_crit'] = 0
                criteria['end_dFVC_crit'] = 0
                criteria['EOFE_crit'] = 0
                criteria['accept'] = 0

            # Manoever accepted
            if criteria['start_of_test_crit'] and criteria['max_insp_crit'] and criteria['EOFE_crit']:
                criteria['accept'] = 1
            else:
                criteria['accept'] = 0


            # Repeatability
            if data['tex'][nTrial] >= 1:
                criteria['repeat_Tex_crit'] = 1
                if data['dFEV1_man'] <= 0.1:
                    criteria['repeat_dFEV1_crit'] = 1
                    criteria['repeat_crit'] = 1
                elif data['dFEV1%_man'] <= 10:
                    criteria['repeat_dFEV1_delta_crit'] = 1
                    criteria['repeat_crit'] = 1
                    criteria['repeat_dFEV1_crit'] = 0
                else:
                    criteria['repeat_dFEV1_delta_crit'] = 0
                    criteria['repeat_crit'] = 0
                    criteria['repeat_dFEV1_crit'] = 0

            elif data['dFEV75_man'] <= 0.1:
                criteria['repeat_dFEV75_crit'] = 1
                criteria['repeat_crit'] = 1
                criteria['repeat_Tex_crit'] = 0

            elif data['dFEV75%_man'] <= 10:
                criteria['repeat_dFEV75_delta_crit'] = 1
                criteria['repeat_crit'] = 1
                criteria['repeat_dFEV75_crit'] = 0
                criteria['repeat_Tex_crit'] = 0

            else:
                criteria['repeat_dFEV75_delta_crit'] = 0
                criteria['repeat_dFEV75_crit'] = 0
                criteria['repeat_Tex_crit'] = 0
                criteria['repeat_crit'] = 0


            if data['dFVC_man'] <= 0.1:
                criteria['repeat_dFVC_crit'] = 1
                if 'repeat_crit' not in criteria: # means that it went in at least one YES above
                    criteria['repeat_crit'] = 1

            elif data['dFVC%_man'] <= 10:
                criteria['repeat_dFVC_delta_crit'] = 1
                criteria['repeat_dFVC_crit'] = 0
            if 'repeat_crit' not in criteria:
                criteria['repeat_crit'] = 1
            else:
                criteria['repeat_dFVC_delta_crit'] = 0
                criteria['repeat_crit'] = 0
                criteria['repeat_dFVC_crit'] = 0

        else:
            # End of forced expiration

            if data['EOTV'][nTrial] < 0.025:
                criteria['end_EOTV_crit'] = 1
                criteria['EOFE_crit'] = 1

            elif data['FET   '][nTrial] >= 15:
                criteria['end_FET_crit'] = 1
                criteria['EOFE_crit'] = 1
                criteria['end_EOTV_crit'] = 0

            elif data['dFVC_man'] <= 0.15:
                criteria['end_dFVC_crit'] = 1
                criteria['EOFE_crit'] = 1
                criteria['end_FET_crit'] = 0
                criteria['end_EOTV_crit'] = 0
            else:
                criteria['end_dFVC_crit'] = 0
                criteria['end_FET_crit'] = 0
                criteria['end_EOTV_crit'] = 0
                criteria['EOFE_crit'] = 0
                criteria['accept'] = 0

        if criteria['start_of_test_crit'] and criteria['max_insp_crit'] and criteria['EOFE_crit']:
            criteria['accept'] = 1
        else:
            criteria['accept'] = 0

        # Repeatability

        if data['dFEV1_man'] <= 0.15:
            criteria['repeat_dFEV1_crit'] = 1
        else:
            criteria['repeat_dFEV1_crit'] = 0
            criteria['repeat_crit'] = 0

        if data['dFVC_man'] <= 0.15:
            criteria['repeat_dFVC_crit'] = 1
            if 'repeat_crit' not in criteria:
                criteria['repeat_crit'] = 1
        else:
            criteria['repeat_dFVC_crit'] = 0
            criteria['repeat_crit'] = 0


        print(nTrial, 'Accepted: ', criteria['accept'])
        criterias[nTrial] = criteria
        if nTrial == 1:
            for key, value in criteria.items():
                print(f'{key: <10}{value}')

    return criterias


def compute_dFEV75man(data):
    # difference between the two largest values --> repeatability criteria ATS/ERS guidelines 2019
    
    # Compute dFEV.75
    v = np.sort(data['FEV.75'])
    data['dFEV75_man'] = v[-1] - v[-2]
    data['dFEV75%_man'] = data['dFEV75_man'] / max(data['FEV.75']) * 100

    return data


def compute_dPEFman(data):

    # difference between the two largest values --> repeatability criteria ATS/ERS guidelines 2019

    # Compute dPEF
    v = np.sort(data['PEF   '])
    data['dPEF_man'] = v[-1] - v[-2]
    data['dPEF%_man'] = data['dPEF_man'] / max(data['PEF   ']) * 100
    return data


def compute_dFEV1man(data):

    # difference between the two largest values --> repeatability criteria ATS/ERS guidelines 2019

    # Compute dPEF
    v = np.sort(data['FEV1 '])
    data['dFEV1_man'] = v[-1] - v[-2]
    data['dFEV1%_man'] = data['dFEV1_man'] / max(data['FEV1 ']) * 100
    return data


def compute_dFVCman(data):

    # difference between the two largest values --> repeatability criteria ATS/ERS guidelines 2019

    # Compute dPEF
    v = np.sort(data['FVC   '])
    data['dFVC_man'] = v[-1] - v[-2]
    data['dFVC%_man'] = data['dFVC_man'] / max(data['FVC   ']) * 100
    return data


def compute_tex(data):
    trialNum = len(data['vol_FV'])
    tex = []
    for nTrial in range(trialNum):

        y = np.array(data['vol_VT'][nTrial])
        x = np.array(data['time_VT'][nTrial])
        #plt.plot(x, y)


        i_peaks, properties = find_peaks(y, height = 0)
        if len(i_peaks):
            i_max_peak = i_peaks[np.argmax(y[i_peaks])]
            #plt.plot(x[i_max_peak], y[i_max_peak], "x")
        idx_start = i_max_peak


        grad = np.gradient(y[i_max_peak:])

        idx_end = len(y)-1
        for i in range(1, len(grad)):
            if grad[i] > 0 and grad[i-1] < grad[i]:
                idx_end = i + i_max_peak
                break

        #plt.plot(x[idx_end], y[idx_end], "x")
        #plt.show()

        tex.append((x[idx_end]-x[idx_start]) * 1e-3) #in secondes

    data['tex'] = tex
    return data
