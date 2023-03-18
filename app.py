from flask import Flask, render_template, request
app = Flask(__name__)
from noiseapp_backend import NoiseApp
noiseapp = NoiseApp()

@app.route('/', methods=('GET', 'POST'))
def index():
    result = 0
    result2 = 0
    safeTime = []
    NRR = ''
    if request.method == 'POST':

        # Get Regulation and Standard
        Regulation = request.form.get("regulation")
        Standard = request.form.get("standard")

        # Get NRR Values
        if request.form.get("hearingProc") == "true":
            NRR = request.form.get("NRR")
        else:
            NRR = 0

        # Fill out arr with LEQ and Time Combinations
        arr = []
        for i in range(1, 11):
            LEQ = int(request.form.get(f"LEQ{i}"))
            TIME = int(request.form.get(f"TIME{i}"))
            arr.append((LEQ, TIME))

        # Set Regulation and Standard Values
        if Regulation == "OSHA":
            noiseapp.setOSHA()
            if Standard == "ES":
                noiseapp.setThreshENGSTD()
            elif Standard == "HCP":
                noiseapp.setThreshHCP()
            else:
                Threshold = int(request.form.get("Threshold"))
                noiseapp.setThreshCUSTOM(Threshold)
        elif Regulation == "NIOSH":
            noiseapp.setNIOSH()
            if Standard == "ES":
                noiseapp.setThreshENGSTD()
            elif Standard == "HCP":
                noiseapp.setThreshHCP()
            else:
                Threshold = int(request.form.get("Threshold"))
                noiseapp.setThreshCUSTOM(Threshold)
        elif Regulation == "CustomRegulation":
            customregulation1 = request.form.get("customregulation1")
            customregulation2 = request.form.get("customregulation2")
            if customregulation1 and customregulation2:
                ER_BASE = float(customregulation1)
                ER_MULT = float(customregulation2)
            noiseapp.setCUSTOM(ER_BASE, ER_MULT)
            if Standard == "ES":
                noiseapp.setThreshENGSTD()
            elif Standard == "HCP":
                noiseapp.setThreshHCP()
            else:
                Threshold = int(request.form.get("Threshold"))
                noiseapp.setThreshCUSTOM(Threshold)

        # Perform Calculations
        percDosage = noiseapp.percentDosageCalc(arr, int(NRR))
        TWA = noiseapp.TWACalc(arr, int(NRR))
        protRec = noiseapp.protectionRec(TWA, int(NRR))
    
    return render_template('index.html', percDosage = percDosage, protRec = protRec)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reginfo')
def reginfo():
    return render_template('regulation_info.html')

@app.route('/moreinfo')
def moreinfo():
    return render_template('more_info.html')
