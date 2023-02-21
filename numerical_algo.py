from datetime import datetime

'''

State: 
- Was implemented in python by translation of the matlab code but without verification of the flowchart --> have to check before usage
- Need to compute dFEV75, dFEV75% and Tex

'''


def flowchart(dataTrial):


    # check if dataTrial contain needed info
    keys_needed = {'TestDate', 'BirthDate', 'VBE%FVC', 'VBEex ', 'FETPEF', 'dPEF_', 'Tdel', 'FVC IN', 'FVC   ', 'EOTV',
                   'FET   ', 'dFVC', 'dFVC%', 'tex', 'dFEV1',  'dFEV1%', 'dFEV_75', 'dFEV_75_'}
    for key in keys_needed:
        if key not in dataTrial.keys():
            print(key, ' is not in dataTrial')


    criteria = dict()
    age = ((datetime.strptime(dataTrial['TestDate'], '%Y-%m-%d')) - (
        datetime.strptime(dataTrial['BirthDate'], '%Y-%m-%d')))
    criteria['age'] = age.days / 365.25

    # Start of test

    # BEV < 5% FVC or < 0.1L
    if dataTrial['VBE%FVC'] < 5:
        criteria['start_VBE_FVC_crit'] = 1
    elif dataTrial['VBEex '] < 0.1:
        criteria['start_VBE_0_1_crit'] = 1
        criteria['start_VBE_FVC_crit'] = 0
    else:
        criteria['start_VBE_0_1_crit'] = 0
        criteria['start_VBE_FVC_crit'] = 0
        criteria['start_of_test_crit'] = 0
        criteria['accept'] = 0

    # FETPEF
    if float(dataTrial['FETPEF']) <= 150:
        criteria['start_FETPEF_crit'] = 1
    else:
        criteria['start_FETPEF_crit'] = 0
        criteria['start_of_test_crit'] = 0
        criteria['accept'] = 0

    # Delta PEF
    '''CHECK HERE'''

    if dataTrial['dPEF_'] <= 10:
        criteria['start_dPEF_10_crit'] = 1
    elif dataTrial['dPEF_'] >= -10:
        criteria['start_dPEF_minus_10_crit'] = 1
        criteria['start_dPEF_10_crit'] = 0
    else:
        criteria['start_dPEF_minus_10_crit'] = 0
        criteria['start_dPEF_10_crit'] = 0
        criteria['start_of_test_crit'] = 0
        criteria['accept'] = 0

    # Hesitation time
    if 'Tdel' in dataTrial:
        if dataTrial['Tdel'] <= 2:
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
    if dataTrial['FVC IN'] - dataTrial['FVC   '] <= 0.1:
        criteria['max_insp_FVCIN_FVC_0_1_crit'] = 1
        criteria['max_insp_crit'] = 1
    elif dataTrial['FVC IN'] - dataTrial['FVC   '] <= 0.05 * dataTrial['FVC   ']:
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

        if dataTrial['EOTV'] < 0.025:
            criteria['end_EOTV_crit'] = 1
            criteria['EOFE_crit'] = 1

        elif dataTrial[ 'FET   '] >= 15:
            criteria['end_FET_crit'] = 1
            criteria['EOFE_crit'] = 1
            criteria['end_EOTV_crit'] = 0

        elif dataTrial['dFVC'] <= 0.1:
            criteria['end_dFVC_crit'] = 1
            criteria['EOFE_crit'] = 1
            criteria['end_FET_crit'] = 0
            criteria['end_EOTV_crit'] = 0

        elif dataTrial['dFVC%'] <= 10:
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
        if dataTrial['tex'] >= 1:
            criteria['repeat_Tex_crit'] = 1
            if dataTrial['dFEV1'] <= 0.1:
                criteria['repeat_dFEV1_crit'] = 1
                criteria['repeat_crit'] = 1
            elif dataTrial['dFEV1%'] <= 10:
                criteria['repeat_dFEV1_delta_crit'] = 1
                criteria['repeat_crit'] = 1
                criteria['repeat_dFEV1_crit'] = 0
            else:
                criteria['repeat_dFEV1_delta_crit'] = 0
                criteria['repeat_crit'] = 0
                criteria['repeat_dFEV1_crit'] = 0

        elif dataTrial['dFEV_75'] <= 0.1:
            criteria['repeat_dFEV75_crit'] = 1
            criteria['repeat_crit'] = 1
            criteria['repeat_Tex_crit'] = 0


        elif dataTrial['dFEV_75_'] <= 10:
            criteria['repeat_dFEV75_delta_crit'] = 1
            criteria['repeat_crit'] = 1
            criteria['repeat_dFEV75_crit'] = 0
            criteria['repeat_Tex_crit'] = 0

        else:
            criteria['repeat_dFEV75_delta_crit'] = 0
            criteria['repeat_dFEV75_crit'] = 0
            criteria['repeat_Tex_crit'] = 0
            criteria['repeat_crit'] = 0


        if dataTrial['dFVC'] <= 0.1:
            criteria['repeat_dFVC_crit'] = 1
            if 'repeat_crit' not in criteria:
                criteria['repeat_crit'] = 1

        elif dataTrial['dFVC_'] <= 10:
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

        if dataTrial['EOTV'] < 0.025:
            criteria['end_EOTV_crit'] = 1
            criteria['EOFE_crit'] = 1

        elif dataTrial['FET   '] >= 15:
            criteria['end_FET_crit'] = 1
            criteria['EOFE_crit'] = 1
            criteria['end_EOTV_crit'] = 0

        elif dataTrial['dFVC'] <= 0.15:
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

    return criteria