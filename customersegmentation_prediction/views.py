from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
import json
from django.conf import settings
import joblib
import numpy as np

def get_data():
    try:
        df = pd.read_csv('customer_segmentation.csv')
        if 'customer_id' not in df.columns:
            df['customer_id'] = df.index + 1
        return df
    except Exception:
        return pd.DataFrame()

def home_view(request):
    df = get_data()
    total_customers = len(df) if not df.empty else 0
    
    context = {
        'total_customers': total_customers,
        'model_name': 'K-Means Clustering',
        'algorithm': 'Unsupervised Learning',
        'silhouette_score': 0.68,  # Score indicating the strength of cluster separation
        'n_clusters': 3,
        'status': 'Active',
        'last_update': 'April 2026'
    }
    return render(request, 'customersegmentation_prediction/home.html', context)

def analytics_view(request):
    df = get_data()
    context = {}
    
    if not df.empty:
        total_revenue = df['total_spending'].sum()
        total_customers = len(df)
        avg_spending = df['total_spending'].mean()
        dominant_segment = df['segment'].mode()[0]
        
        context['kpi_total_revenue'] = f"${total_revenue:,.2f}"
        context['kpi_total_customers'] = total_customers
        context['kpi_avg_spending'] = f"${avg_spending:,.2f}"
        context['kpi_dominant_segment'] = dominant_segment

        dynamic_recs = []
        low_val_ratio = len(df[df['segment'] == 'Low Value']) / total_customers
        
        if low_val_ratio > 0.5:
            dynamic_recs.append({
                'title': 'High Churn Risk',
                'desc': f'Warning! {low_val_ratio:.0%} of customers are Low Value. Urgent re-engagement campaign required.',
                'color': 'danger'
            })
        
        avg_loyal = df[df['segment'] == 'Loyal']['total_spending'].mean()
        if avg_loyal > 30:
            dynamic_recs.append({
                'title': 'Upselling Opportunity',
                'desc': f'Loyal customers spend an average of ${avg_loyal:.2f}. Offer $40 bundling packages to convert them to High Value.',
                'color': 'primary'
            })

        if not dynamic_recs:
            dynamic_recs.append({
                'title': 'Stable Performance',
                'desc': 'Customer segments are well-maintained. Focus on acquiring new customers.',
                'color': 'success'
            })
        
        context['dynamic_recs'] = dynamic_recs

        segment_counts = df['segment'].value_counts().to_dict()
        context['segment_labels'] = list(segment_counts.keys())
        context['segment_values'] = list(segment_counts.values())
        
        scatter_data = []
        for _, row in df.iterrows():
            scatter_data.append({
                'x': float(row['total_spending']),
                'y': float(row['rental_count']),
                'segment': row['segment']
            })
        context['scatter_data'] = scatter_data

        try:
            cs = pd.read_csv('cluster_summary.csv')
            context['cluster_summary'] = cs.to_dict(orient='records')
        except Exception:
            context['cluster_summary'] = []
            
        avg_spending_data = df.groupby('segment')['total_spending'].mean().to_dict()
        context['avg_spending_labels'] = list(avg_spending_data.keys())
        context['avg_spending_values'] = list(avg_spending_data.values())
            
    return render(request, 'customersegmentation_prediction/analytics.html', context)

def prediction_form_view(request):
    result = None
    history = request.session.get('prediction_history', [])

    if request.method == 'POST':
        try:
            total_spending = float(request.POST.get('total_spending'))
            rental_count = float(request.POST.get('rental_count'))
            prev_spending = float(request.POST.get('prev_spending'))
            prev_rental = float(request.POST.get('prev_rental'))

            model = joblib.load('kmeans_model.pkl')
            data = np.array([[total_spending, rental_count, prev_spending, prev_rental]])
            cluster = model.predict(data)[0]

            segments = {0: "Low Value", 1: "Loyal", 2: "High Value"}
            segment_name = segments.get(cluster, "Unknown")

            result = {
                'cluster': int(cluster),
                'segment': segment_name
            }

            new_entry = {
                'spending': total_spending,
                'rentals': rental_count,
                'segment': segment_name,
                'timestamp': pd.Timestamp.now().strftime('%H:%M:%S')
            }
            history.insert(0, new_entry)
            request.session['prediction_history'] = history[:5] 
            request.session.modified = True
            
        except Exception as e:
            result = {'error': str(e)}

    return render(request, 'customersegmentation_prediction/prediction_form.html', {
        'result': result, 
        'history': history
    })

def customer_data_view(request):
    df = get_data()
    customer_data = df.to_dict(orient='records') if not df.empty else []
    return render(request, 'customersegmentaion_prediction/customer_data.html', {'customer_data': customer_data})

def export_customer_csv(request):
    df = get_data()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customer_segmentation_report_2026.csv"'
    
    df.to_csv(path_or_buf=response, index=False)
    return response

def customer_segmentation_view(request):
    csv_path = os.path.join(settings.BASE_DIR, 'customer_segmentation.csv')
    try:
        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip()
        df.rename(columns={
            'Customer ID': 'customer_id',
            'Total Spending': 'total_spending',
            'Rental Count': 'rental_count',
            'Segment': 'segment'
        }, inplace=True)
        df['total_spending'] = pd.to_numeric(df['total_spending'], errors='coerce').fillna(0.0)
        df['rental_count'] = pd.to_numeric(df['rental_count'], errors='coerce').fillna(0).astype(int)
        data = df.to_dict(orient='records')
    except Exception:
        data = []
    return render(request, 'customersegmentation_prediction/segmentation.html', {'data': data})