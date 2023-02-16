import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt

'''Change algo so that if there isn't pre and post sessions it works anyway'''
'''Have to know which one was the best trial'''

'''print code message of the software'''

'''Turn the curves'''


def get_raw_vectors(path, nameFile):
    xmlFile = path + "\\" + nameFile

    # Initialisations
    rawVT = []
    rawFV = []
    time_VT = []
    vol_VT = []
    strTuplesVT = []
    flow_FV = []
    vol_FV = []
    strTuplesFV = []

    # Read XML
    tree = ET.parse(xmlFile)
    root = tree.getroot()

    # Pre trials only : pre Ventolin administration
    levelTrees = root.findall('VisitTrees/VisitTree/Levels/LevelTree/Level[@Type="Pre"]...')
    for levelTree in levelTrees: measurements = levelTree.findall("./Measurements/Measurement[@MeasurementType='Spirometry']")

    for measurement in measurements: trials = measurement.findall("./Trials/Trial")

    for trial in trials :
        number = int(trial.get('Number'))
        curves = trial.findall("./RawCurveData/Curves/Curve")

        # if there is no raw data available for the trial
        if len(curves) == 0:
            print("Trial number ", number, " doesn't contain raw curve data")

        for curve in curves:
            curveType = curve.get('DataType')
            if curveType == 'RawVolumeTime':
                rawVT.append(curve.find("Data").text)
            elif curveType == 'RawFlowVolume':
                rawFV.append(curve.find("Data").text)

    # Transform strings from XML into vectors of floats
    for t in range(len(rawVT)):
        xVT = []
        yVT = []
        xFV = []
        yFV = []

        strTuplesVT.append(rawVT[t].split(' '))
        for n in range(len(strTuplesVT[t]) - 1):
            fTuple = np.fromstring(strTuplesVT[t][n], dtype=float, sep=',')
            xVT.append(fTuple[0])
            yVT.append(fTuple[1])

        strTuplesFV.append(rawFV[t].split(' '))
        for n in range(len(strTuplesFV[t]) - 1):
            fTuple = np.fromstring(strTuplesFV[t][n], dtype=float, sep=',')
            xFV.append(fTuple[0])
            yFV.append(fTuple[1])

        time_VT.append(xVT)
        vol_VT.append(yVT)

        vol_FV.append(xFV)
        flow_FV.append(yFV)

    # mini check data
    if vol_FV == vol_VT:
        print("Volume vectors from the V-T curve and from the F-V are identical")
    else:
        print("WARNING: Volume vectors from the V-T curve and from the F-V are different")

    return vol_VT, time_VT, flow_FV, vol_FV, nameFile


def plot_raw_curves(vol_VT, time_VT, flow_FV, vol_FV, nameFile):

    fig, axs = plt.subplots(2, len(time_VT))

    for resp in range(len(time_VT)):
        axs[0, resp].plot(time_VT[resp], vol_VT[resp], "k")
        axs[0, resp].set_title(f'V-T (#{resp})')
        axs[1, resp].plot(vol_FV[resp], flow_FV[resp], "r")
        axs[1, resp].set_title(f'F-V (#{resp})')

    fig.suptitle(('Example File SentrySuite: ' + nameFile))
    plt.show()


def get_parameters(xmlFile):
    print("THIS FUNCTION IS IN BUILD...")
    data = dict()

    tree = ET.parse(xmlFile)
    root = tree.getroot()

    patient = root.findall("Patient")[0]
    data['ID'] = patient.find("ExternalId").text
    data['LastName'] = patient.find("LastName").text
    data['FirstName'] = patient.find("FirstName").text
    data['BirthDate'] = patient.find("Birthdate").text[0:10]

    visit = root.findall("VisitTrees/VisitTree/Visit")[0]
    data['Sexe'] = visit.find("Gender").text
    data['Weight'] = visit.find("Weight").text
    data['Height'] = visit.find("Height").text
    data['TestDate'] = visit.get("LocalDate")[0:10]
    data['TestTime'] = visit.get("LocalDate")[11:19] # CHECK TIME

    levelTrees = root.findall('VisitTrees/VisitTree/Levels/LevelTree/Level[@Type="Pre"]...')
    for levelTree in levelTrees: measurements = levelTree.findall("./Measurements/Measurement[@MeasurementType='Spirometry']")
    for measurement in measurements: trials = measurement.findall("./Trials/Trial")
    for trial in trials:
        number = int(trial.get('Number'))
        params = trial.findall("./Parameters/Parameter")
        print("In trial", number, ", params: \n")

        keys = []
        vals = []
        for param in params:
            keys.append(param.get('ShortName'))
            vals.append(param.find('Value').text)

        data_param = dict(zip(keys, vals))

        data.update(data_param)

        return data




'''
    NbCurves
    Inhalation
    CurvesOrder
    QualitySpiro
    IdxTrial
    FEV1
    FEV75
    FEV5
    FVC
    FVC_IN
    VC_IN
    VC_MAX
    FEV1_per_FVC
    FEV1_per_VCmax
    FETPEF
    FEF25
    FEF50
    FEF75
    MFEF
    MEF25
    MEF50
    MEF75
    PEF
    PIF
    VBEex
    VBE_per_FVC
    Tdel
    dFEV1
    dFEV1_per_dFVC
    dFVC_per_FET
'''
