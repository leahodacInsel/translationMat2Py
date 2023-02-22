from datetime import datetime
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import numpy as np


def flowchart(data):

    # check if dataTrial contain needed info
    keys_needed = {'TestDate', 'BirthDate', 'VBE%FVC', 'VBEex ', 'FETPEF', 'dPEF_', 'Tdel', 'FVC IN', 'FVC   ', 'EOTV',
                   'FET   ', 'dFVC', 'dFVC%', 'tex', 'dFEV1',  'dFEV1%', 'dFEV_75', 'dFEV_75_'}
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
        elif data['VBEex '][nTrial] < 0.1:
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
        '''CHECK HERE'''

        if data['dPEF_'][nTrial] <= 10:
            criteria['start_dPEF_10_crit'] = 1
        elif data['dPEF_'][nTrial] >= -10:
            criteria['start_dPEF_minus_10_crit'] = 1
            criteria['start_dPEF_10_crit'] = 0
        else:
            criteria['start_dPEF_minus_10_crit'] = 0
            criteria['start_dPEF_10_crit'] = 0
            criteria['start_of_test_crit'] = 0
            criteria['accept'] = 0

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
        if data['FVC IN'][nTrial] - data['FVC   '][nTrial] <= 0.1:
            criteria['max_insp_FVCIN_FVC_0_1_crit'] = 1
            criteria['max_insp_crit'] = 1
        elif data['FVC IN'][nTrial] - data['FVC   '][nTrial] <= 0.05 * data['FVC   '][nTrial]:
            criteria['max_insp_FVCIN_FVC_0_0_5_FVC_crit'] = 1
            criteria['max_insp_crit'] = 1
            criteria['max_insp_FVCIN_FVC_0_1_crit'] = 0
        else:
            criteria['max_insp_FVCIN_FVC_0_0_5_FVC_crit'] = 0
            criteria['max_insp_FVCIN_FVC_0_1_crit'] = 0
            criteria['max_insp_crit'] = 0
            criteria['accept'] = 0

        # Now split by age because it has some differences in criteria
        if float(criteria['age']) <= 6:
            criteria['age_crit'] = 1

            # End of forced expiration
            # volume_change < 0.025 & & volume_change_time >= 1 --> EOTV

            if data['EOTV'][nTrial] < 0.025:
                criteria['end_EOTV_crit'] = 1
                criteria['EOFE_crit'] = 1

            elif data[ 'FET   '][nTrial] >= 15:
                criteria['end_FET_crit'] = 1
                criteria['EOFE_crit'] = 1
                criteria['end_EOTV_crit'] = 0

            elif data['dFVC'][nTrial] <= 0.1:
                criteria['end_dFVC_crit'] = 1
                criteria['EOFE_crit'] = 1
                criteria['end_FET_crit'] = 0
                criteria['end_EOTV_crit'] = 0

            elif data['dFVC%'][nTrial] <= 10:
                criteria['end_dFVC_delta_crit'] = 1
                criteria['EOFE_crit'] = 1
                criteria['end_dFVC_crit'] = 0
                criteria['end_FET_crit'] = 0
                criteria['end_EOTV_crit'] = 0

            else:
                criteria['end_dFVC_delta_crit'] = 0
                criteria['end_dFVC_crit'] = 0
                criteria['end_FET_crit'] = 0
                criteria['end_EOTV_crit'] = 0
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
                if data['dFEV1'][nTrial] <= 0.1:
                    criteria['repeat_dFEV1_crit'] = 1
                    criteria['repeat_crit'] = 1
                elif data['dFEV1%'] <= 10:
                    criteria['repeat_dFEV1_delta_crit'] = 1
                    criteria['repeat_crit'] = 1
                    criteria['repeat_dFEV1_crit'] = 0
                else:
                    criteria['repeat_dFEV1_delta_crit'] = 0
                    criteria['repeat_crit'] = 0
                    criteria['repeat_dFEV1_crit'] = 0

            elif data['dFEV_75'][nTrial] <= 0.1:
                criteria['repeat_dFEV75_crit'] = 1
                criteria['repeat_crit'] = 1
                criteria['repeat_Tex_crit'] = 0


            elif data['dFEV_75_'][nTrial] <= 10:
                criteria['repeat_dFEV75_delta_crit'] = 1
                criteria['repeat_crit'] = 1
                criteria['repeat_dFEV75_crit'] = 0
                criteria['repeat_Tex_crit'] = 0

            else:
                criteria['repeat_dFEV75_delta_crit'] = 0
                criteria['repeat_dFEV75_crit'] = 0
                criteria['repeat_Tex_crit'] = 0
                criteria['repeat_crit'] = 0


            if data['dFVC'][nTrial] <= 0.1:
                criteria['repeat_dFVC_crit'] = 1
                if 'repeat_crit' not in criteria:
                    criteria['repeat_crit'] = 1

            elif data['dFVC_'][nTrial] <= 10:
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

            elif data['dFVC'][nTrial] <= 0.15:
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

        if data['dFEV1'][nTrial] <= 0.15:
            criteria['repeat_dFEV1_crit'] = 1
        else:
            criteria['repeat_dFEV1_crit'] = 0
            criteria['repeat_crit'] = 0

        if data['dFVC'][nTrial] <= 0.15:
            criteria['repeat_dFVC_crit'] = 1
            if 'repeat_crit' not in criteria:
                criteria['repeat_crit'] = 1
        else:
            criteria['repeat_dFVC_crit'] = 0
            criteria['repeat_crit'] = 0


        print(nTrial, 'Accepted: ', criteria['accept'])

    criterias[nTrial] = criteria
    return criterias


def compute_dFEV75(data):
    # difference between the two largest values --> repeatability criteria ATS/ERS guidelines 2019
    
    # Compute dFEV.75
    v = np.sort(data['FEV.75'])
    data['dFEV_75'] = v[-1] - v[-2]
    data['dFEV_75_'] = data['dFEV_75'] / max(data['FEV.75']) * 100

    return data


def compute_dPEF(data):

    '''I thought abuot this as well, but wasnt sure. But I think, for the dPEF it would be: delta between largest
    and "current" trails (so if you want the do QC on the trial n°3, and trial n°1 has the highest PEF, you should
    take these two for the dPEF)'''

    # difference between the two largest values --> repeatability criteria ATS/ERS guidelines 2019

    # Compute dPEF
    data['dPEF'] = max(data['PEF   ']) - data['PEF   ']
    data['dPEF_'] = data['dPEF'] / max(data['PEF   ']) * 100
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
