🛒 Customer Purchasing Decision Prediction using Machine Learning
📌 Overview

This project focuses on predicting whether a customer will purchase a product on an e-commerce platform using machine learning classification techniques. By analyzing various factors such as discounts, user behavior, and product attributes, the system provides accurate predictions to support data-driven business decisions.

🎯 Objectives
Predict customer purchasing decisions (Purchase / No Purchase)
Analyze the impact of different features on buying behavior
Compare multiple machine learning models
Improve prediction accuracy using hyperparameter tuning
🧠 Machine Learning Models Used
Decision Tree – Rule-based classification model
Random Forest – Ensemble model for higher accuracy
Logistic Regression – Probabilistic binary classification

✅ Best Performing Model: Random Forest

Accuracy: 0.999817
AUC Score: 0.9998
📊 Dataset

The dataset is based on e-commerce user interaction data and includes features such as:

User ID
Product ID
Coupon Discount Level
Quantity Discount Level
Time on Page
Added to Cart
Device Type
Product Price
Product Rating
Target Variable: Purchased (0 / 1)


⚙️ Features of the System
User Registration & Login System
Model Training Module
Real-time Prediction System
Feature Encoding & Preprocessing
Performance Evaluation (ROC Curve, Confusion Matrix)
Model Saving & Loading using .pkl files
🏗️ System Architecture

The system consists of:

Frontend: User interface for input and interaction
Backend (Django): Handles logic, authentication, and workflows
Machine Learning Layer: Model training and prediction
Database: Stores user data
Storage: Saves trained models and encoders


🔄 Workflow
User registers and logs in
User can train the model or directly predict
Dataset is preprocessed and model is trained
Model is saved for reuse
User inputs features for prediction
System outputs purchase decision
🛠️ Technologies Used
Python 🐍
Django 🌐
Scikit-learn 🤖
Pandas & NumPy 📊
Matplotlib / Seaborn 📈

📈 Key Insights
Coupon discount and quantity discount are the most influential features
Pricing strategies significantly impact customer decisions
Ensemble models like Random Forest perform better than individual models
🚀 How to Run the Project

# Clone the repository
git clone https://github.com/sairamnaradashi97/Major-Project-Stage-2.git

# Navigate to project folder
cd your-repo-name

# Install dependencies
pip install -r requirements.txt

# Run Django server
python manage.py runserver
📌 Future Improvements
Add deep learning models
Improve UI/UX design
Deploy on cloud (AWS / Heroku)
Real-time recommendation integration
👨‍💻 Author

Sai Ram Naradashi

📄 License

This project is for academic and learning purposes.