# Customer Intelligence System 🚀
**An AI-Powered Customer Segmentation Platform built with Django & Machine Learning.**

## 📌 Project Overview
This project is an end-to-end data science application designed to analyze customer behavioral data from a DVD Rental business. It integrates an **ETL (Extract, Transform, Load)** pipeline with an **Unsupervised Machine Learning** model to segment customers into actionable groups: **High Value**, **Loyal**, and **Low Value**.

## 🛠️ Technical Stack
* **Backend:** Python 3.14+, Django 6.0
* **Machine Learning:** Scikit-Learn (K-Means Clustering), Joblib
* **Data Analysis:** Pandas, NumPy
* **Database:** PostgreSQL (Source) & CSV (Data Lake)
* **Frontend:** HTML5, CSS3 (Bootstrap 5), JavaScript, Chart.js

## ✨ Key Features
* **Executive Dashboard:** Real-time KPI scorecards for Revenue, Customer count, and Segment dominance.
* **Interactive Analytics:** Data visualization using Bar Charts and Scatter Plots.
* **Dynamic AI Recommendations:** Logic-based business strategies that adapt to current data trends.
* **Real-time Prediction AI:** A dedicated tool to predict a new customer's segment based on their metrics.
* **Data Export:** One-click CSV export for marketing team collaboration.
* **Prediction History:** Session-based tracking of recent AI analyses.

## 📊 Model Performance
* **Algorithm:** K-Means Clustering
* **Optimal K:** 3 (Validated via Elbow Method)
* **Silhouette Score:** 0.68 (Indicating strong cluster separation)

## 📁 Project Structure
```text
customersegmentation_project/
│
├── customersegmentation_prediction/  # Main App Folder
│   ├── management/commands/          # ETL Scripts
│   ├── templates/                    # Dashboard UI (HTML/CSS)
│   └── views.py                      # Backend Logic
├── customer_segmentation.csv         # Processed Data
├── kmeans_model.pkl                  # Trained AI Model
├── manage.py                         # Django Entry Point
└── README.md                         # Documentation

## 🚀 How to Run

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
2. Install dependencies:
pip install -r requirements.txt
3. Run ETL Pipeline (Optional):
python manage.py etl_customer_segmentation
4. Start the server:
python manage.py runserver
5. Access the dashboard at http://127.0.0.1:8000
Developed with ❤️ by Puspita Tri Rahayu