def computedFEV75(data):

    trialNum = data['vol_FV']

    for n in range(trialNum):
        # Compute dFEV.75
        v_FEV75.append(dataTrial['trial'+ str(n)][FEV.75])

        dataTrial['dFEV_75'] = max(dataTrial['FEV.75']) - dataTrial['FEV.75']
        dataTrial['dFEV_75_'] = dataTrial['dFEV.75'] / max(dataTrial['FEV.75']) * 100
    return data


def computedPEF(data):
    # Compute dPEF
    dataTrial['dPEF'] = max(dataTrial['PEF']) - dataTrial['PEF']
    dataTrial['dPEF_'] = dataTrial['dPEF'] / max(dataTrial['PEF']) * 100
    return data


def separate_inspi_expi(data):

    data['vol_FV']


    return inspis, expis


