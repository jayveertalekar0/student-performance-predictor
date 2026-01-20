# 📊 Student Performance Predictor

A **machine learning–powered web application** that predicts students’ **Math scores** based on demographic and academic factors.
Built using **Flask, Scikit-learn, and Ensemble Models**, and deployed live on **Render**.

🔗 **Live Application**
👉 [https://student-performance-predictor-ct4p.onrender.com](https://student-performance-predictor-ct4p.onrender.com)

🔗 **GitHub Repository**
👉 [https://github.com/jayveertalekar0/student-performance-predictor](https://github.com/jayveertalekar0/student-performance-predictor)

---

## 🚀 Project Overview

Educational institutions often struggle to identify students who need academic support early.
This project solves that problem by using **machine learning to predict math performance** and classify students into meaningful performance categories.

It demonstrates **end-to-end ML deployment**, from data preprocessing and model training to a fully functional production web app.

---

## ✨ Key Features

* 📈 **ML-Based Prediction**
  Predicts math scores with **90%+ accuracy** using ensemble learning techniques

* ⚡ **Fast & Efficient**
  Predictions generated in **under 2 seconds**

* 📱 **Responsive Web Interface**
  Clean UI accessible across desktop and mobile devices

* 📊 **Dashboard Analytics**
  View prediction history, average scores, and trends

* 🔮 **Performance Categorization**
  Automatically classifies students as:

  * Excellent
  * Good
  * Average
  * Poor

* 🚀 **Production Deployment**
  Deployed on **Render.com** using Gunicorn

---

## 🧠 Machine Learning Details

**Algorithms Used**

* Random Forest
* XGBoost
* CatBoost
  (Combined using Ensemble Learning)

**Model Performance**

* Accuracy: ~90%
* Prediction Time: < 2 seconds

**Input Features**

* Gender
* Race/Ethnicity
* Parental Education Level
* Lunch Type
* Test Preparation Status
* Reading Score (0–100)
* Writing Score (0–100)

**Target Variable**

* Math Score (0–100)

**Dataset**

* 1000+ student records
* Source: Kaggle – Student Performance Dataset

---

## 🎯 Performance Categories

| Score Range | Category     | Description                |
| ----------- | ------------ | -------------------------- |
| 85–100      | Excellent 🎉 | Outstanding performance    |
| 70–84       | Good 👍      | Strong academic foundation |
| 50–69       | Average 📈   | Scope for improvement      |
| 0–49        | Poor 💪      | Needs focused practice     |

---

## 🛠️ Tech Stack

* **Backend:** Flask
* **ML Libraries:** Scikit-learn, XGBoost, CatBoost
* **Data Handling:** Pandas, NumPy
* **Deployment:** Render, Gunicorn
* **Model Serialization:** Joblib

---

## ⚙️ Installation & Local Setup

### Prerequisites

* Python 3.9+
* pip

### Clone the Repository

```bash
git clone https://github.com/jayveertalekar0/student-performance-predictor.git
cd student-performance-predictor
```

### Create Virtual Environment

```bash
python -m venv venv
```

**Activate Environment**

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

Open in browser:

```
http://localhost:5000
```

---

## 🧪 How to Use

### 1️⃣ Make a Prediction

* Navigate to the prediction page
* Enter student details
* Click **“Predict Math Score”**
* View predicted score and performance category

### 2️⃣ Dashboard

* View previous predictions
* Monitor performance trends
* Analyze average scores

---

## 🔧 API Usage

### Endpoint

```
POST /api/predict
```

### Sample Request

```json
{
  "gender": "female",
  "race_ethnicity": "group C",
  "parental_level_of_education": "bachelor's degree",
  "lunch": "standard",
  "test_preparation_course": "completed",
  "reading_score": 85,
  "writing_score": 90
}
```

### Sample Response

```json
{
  "success": true,
  "prediction": 88.5,
  "performance": "Excellent",
  "message": "Outstanding! You're excelling in Mathematics! 🎯"
}
```

---

## 🌐 Deployment (Render)

1. Push code to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. Go to **Render.com**
3. Click **New → Web Service**
4. Connect GitHub repository
5. Configure:

   * Environment: Python 3
   * Build Command: `pip install -r requirements.txt`
   * Start Command: `gunicorn app:app`
6. Deploy 🎉

---

## 🧪 Sample Test Case

| Feature            | Value             |
| ------------------ | ----------------- |
| Gender             | Female            |
| Race               | Group C           |
| Parental Education | Bachelor’s Degree |
| Lunch              | Standard          |
| Test Prep          | Completed         |
| Reading            | 85                |
| Writing            | 90                |

**Expected Output:**
👉 88–92 (Excellent)

---

## 📈 Performance Metrics

* Model Accuracy: **90%+**
* API Response Time: **< 200ms**
* Prediction Time: **< 2 seconds**
* Deployment Uptime: **99.9%**

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgments

* Kaggle Student Performance Dataset
* Flask & Scikit-learn community
* Render.com for free deployment

---

## 📧 Contact

For suggestions or issues, please open a **GitHub Issue**.
⭐ If you like this project, don’t forget to **star the repo**!

---

💡 **This project is resume-ready and demonstrates real-world ML deployment skills.**
