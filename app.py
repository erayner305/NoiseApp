from flask import Flask, render_template, request, session
app = Flask(__name__)
app.secret_key = #Add your own secret key
from noiseapp_backend import NoiseApp
noiseapp = NoiseApp()

# This function checks if the value is numerical and can return a placeholder if it isn't numerical.
# We will be using this function to make sure inputs are acceptable and for error-catching.
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
            # Get NRR Values from user
            if request.form.get("hearingProc") == "true":
                NRR = numCheck(request.form.get("NRR"), 7)
            else:
                NRR = 7

            # Get LEQ and TIME values from user and combine them into an arr
            arr = []
            for i in range(1, 11):
                LEQ = (request.form.get(f"LEQ{i}"))
                TIME = (request.form.get(f"TIME{i}"))
                arr.append((int(LEQ), int(TIME)))
            
            # We are using percentDosageCalc, TWACalc, and protectionRec from the noiseapp.backend file
            # percDosage and protRec are returned to the user to show their exposure and provide a recommendation
            percDosage = noiseapp.percentDosageCalc(arr, int(NRR))
            TWA = noiseapp.TWACalc(arr, int(NRR))
            protRec = noiseapp.protectionRec(TWA, int(NRR))
            
            # We are storing those calculations that we performed earlier using Flask's session support
            # We can return these stored session values to maintain state
            session['percDosage'] = percDosage
            session['TWA'] = TWA
            session['protRec'] = protRec

            return render_template('index.html', percDosage = percDosage, protRec = protRec)
        
        # Catch overflow errors if user tries inputting too large LEQ or Time
        except OverflowError:
            return render_template('index.html', error = "There is an overflow error")
        
        # Catch value errors if user leaves field(s) empty
        except ValueError:
            return render_template('index.html',  error = "There is a value error")

        # All other errors
        except:
            return render_template('index.html', error = "Something went wrong, please try again.")
        
    # Return the state values that we saved earlier if they are available
    return render_template('index.html', percDosage = session.get('percDosage'), protRec = session.get('protRec'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/reginfo')
def reginfo():
    return render_template('regulation_info.html')

@app.route('/moreinfo')
def moreinfo():
    return render_template('more_info.html')
