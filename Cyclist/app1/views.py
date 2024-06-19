from django.shortcuts import render
from app1.models import Rider,Features,Prediction_Output
import joblib
import requests
# import sklearn

# Variables Declaration.
BodyMassIndex = 0.00
height = 0.00
weight = 0.00
mass = 0.00
name = str()
entries = list()
val1 = 0.00
val2 = 0.00

# Create your views here.

def home(request):
    return render(request, 'index.html')

def model(request):
    global name
    name = request.POST['name']
    email = request.POST['email']
    global height
    height = float(request.POST['height'])
    global weight
    weight = float(request.POST['weight'])
    
    global BodyMassIndex
    BodyMassIndex = weight / (height/100)**2
    global mass
    mass = weight / 9.8
    print(mass)
    print(BodyMassIndex)
 

    obj1 = Rider(
        RiderName = name, 
        RiderMail= email, 
        RiderHeight = height, 
        RiderWeight = weight,
        RiderBMI = BodyMassIndex,
        RiderMass = mass,
        )
    obj1.save()
       
    global entries
    entries = thing_speak_data(request)
    
    print(entries)
    
    global val1,val2
    obj2 = Features(
        RiderName = name, 
        RiderBMI = BodyMassIndex,
        RiderMass = mass,
        RiderAcceleration = val2,
        RiderAppliedForce = val1
    )
    obj2.save()
    
    val = {'name':name,'mass':mass, 'BMI':BodyMassIndex ,'entries':entries}
    return render(request, 'model.html', val)


def prediction(request):
    # rgr1 = joblib.load('linear.sav')
    # rgr2 = joblib.load('decision.sav')
    rgr3 = joblib.load('random.sav')
    # rgr4 = joblib.load('support.sav')
    # rgr5 = joblib.load('kneighbors.sav')
    
    lis = []
    
    
    # Initialize the scaler 
    # scaler = StandardScaler()

    # # Fit and transform the training set
    # X_train_scaled = scaler.fit_transform([lis])
    global BodyMassIndex
    # print(BodyMassIndex)
    lis.append(BodyMassIndex)
    global mass
    # print(mass)
    lis.append(mass)
    global val2
    # print(float(val2))
    lis.append(float(val2))
    
    # print(lis)
    
    # ans1 = rgr1.predict([lis])
    # ans2 = rgr2.predict([lis])
    ans3 = rgr3.predict([lis])
    # ans4 = rgr4.predict([lis])
    # ans5 = rgr5.predict([lis])
    
    
    # print(type(val1))
    # print(val1)
    print(type(ans3))
    print(ans3)
    
    pred = (ans3.item())/9.8
    
    # print(type(pred))
    # print(pred)
    
    diff = float(float(val1) - pred)
    
    
    obj3 = Prediction_Output(
        RiderName = name,
        RiderAppliedForce = val1,
        RiderPredictedForce = ans3,
        ForceDifference = diff,
    )
    
    obj3.save()
    
    
    # print(diff)
    if diff < 0.0:
        condition1 = 1
        condition2 = 0
        condition3 = 0
    elif diff <= 1.0:
        condition1 = 0
        condition2 = 2
        condition3 = 0
    elif diff > 1.0:
        condition1 = 0
        condition2 = 0
        condition3 = 3
        
    display = {
        'name':name, 
        # 'ans1':ans1,
        # 'ans2':ans2,
        'ans3':pred,
        # 'ans4':ans4,
        # 'ans5':ans5, 
        'BMI':BodyMassIndex, 
        'mass':mass, 
        'acceleration':val2, 
        'force':val1, 
        'condition1' : condition1,
        'condition2' : condition2,
        'condition3' : condition3,
        'diff' : diff,
    }
    
    return render(request, 'prediction.html', display)


    
def thing_speak_data(request):
    api_key = 'S1CO1OM6N5CX1IE8'
    url = f'https://api.thingspeak.com/channels/2185632/feeds.json?api_key={api_key}'

    # Make an HTTP GET request to the ThingSpeak API endpoint
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the data from the API response
        data = response.json()
        
        # Extract the entries from the data
        
        entries = data['feeds']
        
        entries = entries[-1:-6:-1]    
        print(len(entries))
        print(type(entries))
        
        global val1
        val1 = entries[0]['field1']
        print("val1 :",val1)
        global val2
        val2 = entries[0]['field2']
        print("val2 :",val2)
        
        # Pass the entries to the template for rendering
        return entries
    else:
        # Handle the case when the API request fails
        error_message = f"API request failed with status code: {response.status_code}"
        return render(request, 'error.html', {'error_message': error_message})
