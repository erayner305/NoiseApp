from flask import Flask, render_template, request
app = Flask(__name__)
from noiseapp_backend import NoiseApp
noiseapp = NoiseApp()

# Numeric Checker
def numCheck(value, default_value):
    try:
        return float(value)
    except:
        return default_value

@app.route('/', methods=('GET', 'POST'))
def index():
    NRR = ''
    if request.method == 'POST':

        # Get Regulation and Standard
        Regulation = request.form.get("regulation")
        Standard = request.form.get("standard")

        # Regulations Dictionary
        regulation_dict = {
        "OSHA": noiseapp.setOSHA,
        "NIOSH": noiseapp.setNIOSH,
        "CustomRegulation": lambda: noiseapp.setCUSTOM(
            numCheck(request.form.get(("customregulation1")), 0),
            numCheck(request.form.get(("customregulation2")), 0))
        }

        # Set Regulation
        if Regulation in regulation_dict:
            regulation_dict[Regulation]()

        # Standards Dictionary
        standard_dict = {
        "ES": noiseapp.setThreshENGSTD,
        "HCP": noiseapp.setThreshHCP,
        "CustomStandard": lambda: noiseapp.setThreshCUSTOM(
            numCheck((request.form.get("Threshold")), 0))
        }

        # Set Standards
        if Standard in standard_dict:
            standard_dict[Standard]()

        # Perform Calculations
        try:
            # Get NRR Values
            if request.form.get("hearingProc") == "true":
                NRR = numCheck(request.form.get("NRR"), 7)
            else:
                NRR = 7

            # Fill out arr with LEQ and Time Combinations
            arr = []
            for i in range(1, 11):
                LEQ = (request.form.get(f"LEQ{i}"))
                TIME = (request.form.get(f"TIME{i}"))
                arr.append((int(LEQ), int(TIME)))
            
            # Perform Calculations
            percDosage = noiseapp.percentDosageCalc(arr, int(NRR))
            TWA = noiseapp.TWACalc(arr, int(NRR))
            protRec = noiseapp.protectionRec(TWA, int(NRR))

            return render_template('index.html', percDosage = percDosage, protRec = protRec)
        
        # Numbers too big
        except OverflowError:
            return render_template('index.html', percDosage = "Your exposure is too high and you might die." , protRec = "N/A")
        
        # Empty field(s)
        except ValueError:
            return render_template('index.html', percDosage = "Something went wrong. Make sure there are no empty fields and try again." , protRec = "N/A")

        # All other errors
        except:
            return render_template('index.html', percDosage = "Something went wrong, please try again." , protRec = "N/A")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reginfo')
def reginfo():
    return render_template('regulation_info.html')

@app.route('/moreinfo')
def moreinfo():
    return render_template('more_info.html')
