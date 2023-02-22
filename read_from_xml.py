import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt



def get_parameters(data, path, nameFile):
    xmlFile = path + "\\" + nameFile

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
    if not levelTrees:
        levelTrees = root.findall('VisitTrees/VisitTree/Levels/LevelTree/Level[@Type="ProvBase"]...')
    for levelTree in levelTrees: measurements = levelTree.findall("./Measurements/Measurement[@MeasurementType='Spirometry']")
    for measurement in measurements: trials = measurement.findall("./Trials/Trial")
    keys = []

    for idx_t, trial in enumerate(trials):
        params = trial.findall("./Parameters/Parameter")
        for idx_p, param in enumerate(params):
            if idx_t == 0:
                keys.append(param.get('ShortName'))
                if idx_p == 0:
                    vals = np.empty((len(params), len(trials)))
            vals[idx_p, idx_t] = (float(param.find('Value').text))
    data_param = dict(zip(keys, vals))
    data.update(data_param)

    return data


def get_raw_vectors(data, path, nameFile):
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
    if not levelTrees:
        levelTrees = root.findall('VisitTrees/VisitTree/Levels/LevelTree/Level[@Type="ProvBase"]...')

    for levelTree in levelTrees: measurements = levelTree.findall("./Measurements/Measurement[@MeasurementType='Spirometry']")
    for measurement in measurements: trials = measurement.findall("./Trials/Trial")
    for trial in trials :
        number = int(trial.get('Number'))
        curves = trial.findall("./RawCurveData/Curves/Curve")

        # if there is no raw data available for the trial
        #if len(curves) == 0:
            #print("Trial number ", number, " doesn't contain raw curve data")

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
    if vol_FV != vol_VT:
        print("WARNING: Volume vectors from the V-T curve and from the F-V are different")

    data['vol_VT'] = vol_VT
    data['time_VT'] = time_VT
    data['flow_FV'] = flow_FV
    data['vol_FV'] = vol_FV

    return data


def plot_raw_curves(data, nameFile: object) -> object:
    vol_VT = data['vol_VT']
    time_VT = data['time_VT']
    flow_FV = data['flow_FV']
    vol_FV = data['vol_FV']

    fig, axs = plt.subplots(2, len(time_VT))

    for trial in range(len(time_VT)):

        axs[0, trial].plot(time_VT[trial], vol_VT[trial], "k")
        axs[0, trial].set_title(f'V-T (#{trial})')
        axs[0, trial].tick_params(left=False, right=False, labelleft=False,
                        labelbottom=False, bottom=False)

        axs[1, trial].plot(vol_FV[trial], flow_FV[trial], "r")
        axs[1, trial].set_title(f'F-V (#{trial})')
        #axs[1, trial].set_xlim(-2000, 2000)
        #axs[1, trial].set_ylim(-3000, 5000)
        #axs[1, trial].set_aspect(2)
        axs[1, trial].invert_xaxis()
        axs[1, trial].invert_yaxis()
        axs[1, trial].tick_params(left=False, right=False, labelleft=False,
                        labelbottom=False, bottom=False)



    fig.suptitle(('File SentrySuite: ' + nameFile))
    plt.show()
