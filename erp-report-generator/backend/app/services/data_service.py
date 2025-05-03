import pandas as pd
import io
from datetime import datetime
import calendar
from collections import defaultdict
import numpy as np

class DataService:
    @staticmethod
    def convert_numpy_types(obj):
        """Convert NumPy data types to Python native types for JSON serialization"""
        if isinstance(obj, (np.integer)):
            return int(obj)
        elif isinstance(obj, (np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, dict):
            return {k: DataService.convert_numpy_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [DataService.convert_numpy_types(i) for i in obj]
        else:
            return obj
    
    @staticmethod
    def process_csv_data(file_content: bytes):
        """Process uploaded CSV data"""
        try:
            # Read CSV from bytes
            df = pd.read_csv(io.BytesIO(file_content))
            
            # Ensure required columns exist
            required_columns = ['date', 'product_name', 'units_sold', 'revenue']
            for col in required_columns:
                if col not in df.columns:
                    raise ValueError(f"Missing required column: {col}")
            
            # Convert data to proper types
            df['date'] = pd.to_datetime(df['date'])
            df['units_sold'] = df['units_sold'].astype(int)
            df['revenue'] = df['revenue'].astype(float)
            
            if 'inventory_level' in df.columns:
                df['inventory_level'] = df['inventory_level'].astype(int)
            
            return df
        except Exception as e:
            raise ValueError(f"Error processing CSV: {str(e)}")
    
    @staticmethod
    def analyze_data(df: pd.DataFrame):
        """Analyze the data and generate metrics"""
        metrics = {}
        
        # Sort by date
        df = df.sort_values('date')
        
        # Extract date range
        start_date = df['date'].min()
        end_date = df['date'].max()
        metrics['date_range'] = {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }
        
        # Get unique months in the data
        df['month'] = df['date'].dt.to_period('M')
        months = df['month'].unique()
        
        # Monthly performance
        monthly_data = []
        for month in months:
            month_df = df[df['month'] == month]
            month_name = calendar.month_name[month.month]
            monthly_data.append({
                'month': f"{month_name} {month.year}",
                'total_revenue': month_df['revenue'].sum(),
                'total_units': month_df['units_sold'].sum(),
                'avg_unit_price': month_df['revenue'].sum() / month_df['units_sold'].sum()
            })
        
        metrics['monthly_performance'] = monthly_data
        
        # Calculate month-over-month changes
        if len(monthly_data) >= 2:
            current = monthly_data[-1]
            previous = monthly_data[-2]
            
            revenue_change = ((current['total_revenue'] - previous['total_revenue']) / 
                              previous['total_revenue']) * 100
            units_change = ((current['total_units'] - previous['total_units']) / 
                           previous['total_units']) * 100
            
            metrics['mom_changes'] = {
                'revenue_change_percent': revenue_change,
                'units_change_percent': units_change
            }
        
        # Top selling products
        product_sales = df.groupby('product_name').agg({
            'units_sold': 'sum',
            'revenue': 'sum'
        }).reset_index()
        
        product_sales = product_sales.sort_values('revenue', ascending=False)
        
        metrics['top_products'] = product_sales.head(3).to_dict('records')
        metrics['total_revenue'] = df['revenue'].sum()
        
        # Inventory warnings (if available)
        if 'inventory_level' in df.columns:
            latest_inventory = df.sort_values('date').groupby('product_name')['inventory_level'].last()
            low_inventory = latest_inventory[latest_inventory <= 10].to_dict()
            out_of_stock = latest_inventory[latest_inventory == 0].to_dict()
            
            metrics['inventory_warnings'] = {
                'low_inventory': low_inventory,
                'out_of_stock': out_of_stock
            }
        
        # Regional performance (if available)
        if 'region' in df.columns:
            region_sales = df.groupby('region').agg({
                'units_sold': 'sum',
                'revenue': 'sum'
            }).reset_index()
            
            region_sales = region_sales.sort_values('revenue', ascending=False)
            metrics['regional_performance'] = region_sales.to_dict('records')
        
        # Category performance (if available)
        if 'category' in df.columns:
            category_sales = df.groupby('category').agg({
                'units_sold': 'sum',
                'revenue': 'sum'
            }).reset_index()
            
            category_sales = category_sales.sort_values('revenue', ascending=False)
            metrics['category_performance'] = category_sales.to_dict('records')
        
        # Convert all NumPy types to Python native types for JSON serialization
        metrics = DataService.convert_numpy_types(metrics)
        
        return metrics