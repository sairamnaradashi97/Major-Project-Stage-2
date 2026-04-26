from django.shortcuts import render

import os
from django.conf import settings
from django.shortcuts import render, redirect
from .models import UserRegistrationModel
from django.contrib import messages

def UserRegisterActions(request):
    if request.method == 'POST':
        user = UserRegistrationModel(
            name=request.POST['name'],
            loginid=request.POST['loginid'],
            password=request.POST['password'],
            mobile=request.POST['mobile'],
            email=request.POST['email'],
            locality=request.POST['locality'],
            address=request.POST['address'],
            city=request.POST['city'],
            state=request.POST['state'],
            status='waiting'
        )
        user.save()
        messages.success(request,"Registration successful!")
    return render(request, 'UserRegistrations.html') 


def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginid')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = UserRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                data = {'loginid': loginid}
                print("User id At", check.id, status)
                return render(request, 'users/UserHomePage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'UserLogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'UserLogin.html', {})

def UserHome(request):
    return render(request, 'users/UserHomePage.html', {})


def index(request):
    return render(request,"index.html")



 

# Create your views here.
import os
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use('Agg')  # For headless servers
import matplotlib.pyplot as plt
import seaborn as sns
from django.shortcuts import render
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Training View ----
def train_model(request):
    df = pd.read_csv(os.path.join(BASE_DIR, 'ecommerce_prediction_dataset_with_target.csv'))
    df_ml = df.copy()

    categorical_columns = ['Coupon Discount Level', 'Quantity Discount Level',
                           'Added to Cart', 'Time of Interaction', 'Device']
    label_encoders = {}
    for col in categorical_columns:
        le = LabelEncoder()
        df_ml[col] = le.fit_transform(df_ml[col])
        label_encoders[col] = le

    X = df_ml.drop(columns=['User ID', 'Product ID', 'Purchased'])
    y = df_ml['Purchased']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X_test)
    y_prob = rf_model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    roc_auc = roc_auc_score(y_test, y_prob)

    # Confusion Matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(BASE_DIR, 'static/confusion_matrix.png'))
    plt.close()

    # ROC Curve
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    plt.figure(figsize=(5, 4))
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.4f}")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.title("ROC Curve")
    plt.legend()
    plt.savefig(os.path.join(BASE_DIR, 'static/roc_curve.png'))
    plt.close()

    # Save model
    joblib.dump(rf_model, os.path.join(BASE_DIR, 'random_forest_purchase_model.pkl'))

    context = {
        'accuracy': acc,
        'roc_auc': roc_auc,
        'report': report
    }
    return render(request, 'users/train.html', context)

# ---- Prediction View ----
def predict_view(request):
    prediction = None
    prob = None

    if request.method == 'POST':
        input_data = {
            'Coupon Discount Level': request.POST.get('coupon'),
            'Quantity Discount Level': request.POST.get('quantity'),
            'Time on Page (seconds)': int(request.POST.get('time')),
            'Added to Cart': request.POST.get('cart'),
            'Time of Interaction': request.POST.get('interaction'),
            'Device': request.POST.get('device'),
            'Product Price ($)': float(request.POST.get('price')),
            'Product Rating (stars)': float(request.POST.get('rating'))
        }

        # Load model and encoders
        model = joblib.load(os.path.join(BASE_DIR, 'random_forest_purchase_model.pkl'))
        label_encoders = joblib.load(os.path.join(BASE_DIR, 'label_encoders.pkl'))

        # Encode input
        for col in label_encoders:
            encoder = label_encoders[col]
            val = input_data[col]
            if val in encoder.classes_:
                input_data[col] = encoder.transform([val])[0]
            else:
                # Handle unseen label
                encoder.classes_ = np.append(encoder.classes_, val)
                input_data[col] = encoder.transform([val])[0]

        # Prepare features
        features = [
            'Coupon Discount Level', 'Quantity Discount Level',
            'Time on Page (seconds)', 'Added to Cart', 'Time of Interaction',
            'Device', 'Product Price ($)', 'Product Rating (stars)'
        ]

        X = pd.DataFrame([input_data])[features]
        prediction = model.predict(X)[0]
        prob = model.predict_proba(X)[0][1]

    return render(request, 'users/predict.html', {
'prediction': 'Customer Likely to Purchase' if prediction == 1 else 'Customer Unlikely to Purchase' if prediction is not None else '',
        'probability': prob
    })



