from flask import Flask, render_template, request, session
app = Flask(__name__)
app.secret_key = #Add your own secret key.
from noiseapp_backend import NoiseApp
noiseapp = NoiseApp()

# This function checks if the value is numerical and can return a placeholder if it isn't numerical.
# We will be using this function to make sure inputs are acceptable and for error-catching.
def numCheck(value, default_value):
    try:
        return float(value)
    except ValueError:
        return default_value

@app.route('/', methods=('GET', 'POST'))
def index():
    NRR = ''
    if request.method == 'POST':

        # Get Regulation and Standard from submitted form
        Regulation = request.form.get("regulation")
        Standard = request.form.get("standard")

        # Regulations Dictionary to map user input to its proper regulation
        regulation_dict = {
        "OSHA": noiseapp.setOSHA,
        "NIOSH": noiseapp.setNIOSH,
        # Using numCheck to catch errors from inputting non-numerical values for ERBase, ERMult
        "CustomRegulation": lambda: noiseapp.setCUSTOM(
            numCheck(request.form.get("customregulation1"), 90),
            numCheck(request.form.get("customregulation2"), 5))
        }

        # Set Regulation based on user input
        if Regulation in regulation_dict:
            regulation_dict[Regulation]()

        # Standards Dictionary to map user input to its proper standard
        standard_dict = {
        "ES": noiseapp.setThreshENGSTD,
        "HCP": noiseapp.setThreshHCP,
        # Using numCheck to catch errors from inputting non-numerical values for Threshold
        "CustomStandard": lambda: noiseapp.setThreshCUSTOM(
            numCheck(request.form.get("Threshold"), 90))
        }

        # Set Standards based on user input
        if Standard in standard_dict:
            standard_dict[Standard]()

        # Perform Calculations
        try:
            # Get NRR Values from submitted form
            if request.form.get("hearingProc") == "true":
                # Using numCheck to catch errors from inputting non-numerical values for NRR 
                NRR = numCheck(request.form.get("NRR"), 7)
            else:
                # If no NRR was input, we default to 7
                NRR = 7

            # Iterate through the form and append LEQ, TIME pairs into a list
            arr = []
            for i in range(1, 11):
                # Using numCheck to catch errors from inputting non-numerical values into LEQ, TIME
                LEQ = numCheck(request.form.get(f"LEQ{i}"), 0)
                TIME = numCheck(request.form.get(f"TIME{i}"), 0)
                arr.append((int(LEQ), int(TIME)))
            
            # We are using percentDosageCalc, TWACalc, and protectionRec from the noiseapp.backend file
            # percDosage and protRec are returned to the user to show their exposure and provide a recommendation
            percDosage = noiseapp.percentDosageCalc(arr, int(NRR))
            TWA = noiseapp.TWACalc(arr, int(NRR))
            protRec = noiseapp.protectionRec(TWA, int(NRR))

            # We are storing those calculations that we performed earlier using Flask's session support
            # We can then use these stores session values to maintain state
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
