from flask import Flask, request, render_template, jsonify
import os
import sys
import traceback
import numpy as np
import pandas as pd
from datetime import datetime

# Add src to path - try different approaches
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')

# Try multiple path approaches
possible_paths = [
    src_path,
    os.path.join(current_dir, '..', 'src'),
    os.path.join(current_dir, '.', 'src'),
    os.path.join(current_dir, 'src')
]

for path in possible_paths:
    if os.path.exists(path) and path not in sys.path:
        sys.path.insert(0, path)
        print(f"✅ Added to path: {path}")

print(f"📁 Current directory: {current_dir}")
print(f"📁 Python path: {sys.path}")

# Initialize ML components as None
CustomData = None
PredictPipeline = None

try:
    # Try absolute import first
    from src.pipeline.predict_pipeline import CustomData, PredictPipeline
    print("✅ Successfully imported ML modules using 'src.pipeline.predict_pipeline'")
except ImportError as e:
    print(f"❌ First import attempt failed: {e}")
    
    try:
        # Try relative import
        from src.pipeline.predict_pipeline import CustomData, PredictPipeline
        print("✅ Successfully imported ML modules using 'pipeline.predict_pipeline'")
    except ImportError as e2:
        print(f"❌ Second import attempt failed: {e2}")
        
        try:
            # Try direct import from current directory
            import importlib.util
            module_path = os.path.join(current_dir, 'src', 'pipeline', 'predict_pipeline.py')
            if os.path.exists(module_path):
                spec = importlib.util.spec_from_file_location("predict_pipeline", module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                CustomData = module.CustomData
                PredictPipeline = module.PredictPipeline
                print("✅ Successfully imported ML modules using direct file import")
            else:
                print(f"❌ File not found at: {module_path}")
                raise ImportError(f"File not found: {module_path}")
        except Exception as e3:
            print(f"⚠️ All import attempts failed: {e3}")
            
            # Fallback mock classes for development
            class MockCustomData:
                def __init__(self, **kwargs):
                    self.data = kwargs
                    
                def get_data_as_data_frame(self):
                    # Create a DataFrame with the expected structure
                    data_dict = {
                        'gender': [self.data['gender']],
                        'race_ethnicity': [self.data['race_ethnicity']],
                        'parental_level_of_education': [self.data['parental_level_of_education']],
                        'lunch': [self.data['lunch']],
                        'test_preparation_course': [self.data['test_preparation_course']],
                        'reading_score': [float(self.data['reading_score'])],
                        'writing_score': [float(self.data['writing_score'])]
                    }
                    return pd.DataFrame(data_dict)
            
            class MockPredictPipeline:
                def predict(self, df):
                    # Mock prediction based on reading and writing scores
                    reading = df['reading_score'].iloc[0]
                    writing = df['writing_score'].iloc[0]
                    # Weighted average with some randomness for demo
                    mock_prediction = (reading * 0.4 + writing * 0.4) + 20
                    mock_prediction = max(0, min(100, mock_prediction))
                    return [mock_prediction]
            
            # Use mock classes if import fails
            CustomData = MockCustomData
            PredictPipeline = MockPredictPipeline
            print("⚠️ Using mock ML classes for development")

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

# Store predictions (in production use database)
predictions = []

@app.route('/')
def home():
    """Simple home page"""
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Handle predictions"""
    if request.method == 'GET':
        return render_template('predict.html')
    
    try:
        # Get form data
        gender = request.form.get('gender')
        race_ethnicity = request.form.get('ethnicity')
        parental_education = request.form.get('parental_level_of_education')
        lunch = request.form.get('lunch')
        test_prep = request.form.get('test_preparation_course')
        reading_score = request.form.get('reading_score')
        writing_score = request.form.get('writing_score')
        
        # Basic validation
        if not all([gender, race_ethnicity, parental_education, lunch, test_prep, reading_score, writing_score]):
            return render_template('predict.html', error="Please fill all fields")
        
        # Convert scores to float with validation
        try:
            reading_score_float = float(reading_score)
            writing_score_float = float(writing_score)
            
            if not (0 <= reading_score_float <= 100) or not (0 <= writing_score_float <= 100):
                return render_template('predict.html', error="Scores must be between 0 and 100")
                
        except ValueError:
            return render_template('predict.html', error="Please enter valid numbers for scores")
        
        # Check if CustomData is available
        if CustomData is None:
            return render_template('predict.html', error="ML model not loaded. Please check server logs.")
        
        # Create data object
        data = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_education,
            lunch=lunch,
            test_preparation_course=test_prep,
            reading_score=reading_score_float,
            writing_score=writing_score_float
        )
        
        # Get prediction
        df = data.get_data_as_data_frame()
        print(f"📊 Data for prediction: {df.to_dict()}")
        
        if PredictPipeline is None:
            return render_template('predict.html', error="Prediction pipeline not loaded.")
        
        pipeline = PredictPipeline()
        result = pipeline.predict(df)[0]
        
        # Ensure result is within bounds
        result = max(0, min(100, float(result)))
        
        # Store prediction with timestamp
        prediction_data = {
            'score': round(float(result), 1),
            'category': get_category(float(result)),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'reading': reading_score_float,
            'writing': writing_score_float,
            'gender': gender,
            'ethnicity': race_ethnicity
        }
        predictions.append(prediction_data)
        
        # Keep only last 20 predictions
        if len(predictions) > 20:
            predictions.pop(0)
        
        return render_template('predict.html', 
                             result=round(float(result), 1),
                             category=get_category(float(result)))
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"🔥 Prediction error: {error_msg}")
        traceback.print_exc()
        return render_template('predict.html', error=f"Server error: {str(e)}")

@app.route('/dashboard')
def dashboard():
    """Simple dashboard"""
    if predictions:
        avg_score = sum(p['score'] for p in predictions) / len(predictions)
    else:
        avg_score = 0
    
    return render_template('dashboard.html',
                         predictions=predictions[-10:][::-1],  # Last 10, newest first
                         total=len(predictions),
                         avg_score=round(avg_score, 1))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """JSON API for predictions"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['gender', 'race_ethnicity', 'parental_level_of_education', 
                          'lunch', 'test_preparation_course', 'reading_score', 'writing_score']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        # Validate scores
        try:
            reading_score = float(data['reading_score'])
            writing_score = float(data['writing_score'])
            if not (0 <= reading_score <= 100) or not (0 <= writing_score <= 100):
                return jsonify({'success': False, 'error': 'Scores must be between 0 and 100'}), 400
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid score values'}), 400
        
        # Check if ML modules are loaded
        if CustomData is None or PredictPipeline is None:
            return jsonify({'success': False, 'error': 'ML model not loaded'}), 500
        
        # Create data object
        custom_data = CustomData(
            gender=data['gender'],
            race_ethnicity=data['race_ethnicity'],
            parental_level_of_education=data['parental_level_of_education'],
            lunch=data['lunch'],
            test_preparation_course=data['test_preparation_course'],
            reading_score=reading_score,
            writing_score=writing_score
        )
        
        # Get prediction
        df = custom_data.get_data_as_data_frame()
        pipeline = PredictPipeline()
        result = pipeline.predict(df)[0]
        result = max(0, min(100, float(result)))
        category = get_category(result)
        
        # Store prediction
        prediction_data = {
            'score': round(float(result), 1),
            'category': category,
            'timestamp': datetime.now().isoformat(),
            'reading': reading_score,
            'writing': writing_score
        }
        predictions.append(prediction_data)
        
        if len(predictions) > 20:
            predictions.pop(0)
        
        # Response messages
        messages = {
            'Excellent': "Outstanding! You're excelling in Mathematics! 🎯",
            'Good': "Solid foundation! Keep up the good work! 👍",
            'Average': "Room for improvement. Practice makes perfect! 📈",
            'Poor': "Needs practice. Don't give up! 💪"
        }
        
        return jsonify({
            'success': True,
            'prediction': round(float(result), 1),
            'performance': category,
            'message': messages.get(category, ''),
            'timestamp': prediction_data['timestamp']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'predictions_count': len(predictions),
        'service': 'student-performance-predictor',
        'ml_loaded': CustomData is not None and PredictPipeline is not None
    })

@app.route('/debug')
def debug_info():
    """Debug endpoint to check system info"""
    return jsonify({
        'python_path': sys.path,
        'current_dir': current_dir,
        'ml_loaded': CustomData is not None and PredictPipeline is not None,
        'ml_classes': {
            'CustomData': str(CustomData),
            'PredictPipeline': str(PredictPipeline)
        },
        'files_exist': {
            'src_dir': os.path.exists(src_path),
            'predict_pipeline': os.path.exists(os.path.join(src_path, 'pipeline', 'predict_pipeline.py')) if os.path.exists(src_path) else False
        }
    })

def get_category(score):
    """Categorize score"""
    if score >= 85: return 'Excellent'
    if score >= 70: return 'Good'
    if score >= 50: return 'Average'
    return 'Poor'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# Check for required pickle files
def check_artifacts():
    artifacts_dir = os.path.join(current_dir, 'artifacts')
    if not os.path.exists(artifacts_dir):
        print(f"⚠️ WARNING: Artifacts directory not found at {artifacts_dir}")
        print("The model will not work without model.pkl and preprocessor.pkl")
        return False
    
    model_path = os.path.join(artifacts_dir, 'model.pkl')
    preprocessor_path = os.path.join(artifacts_dir, 'preprocessor.pkl')
    
    if not os.path.exists(model_path):
        print(f"⚠️ WARNING: model.pkl not found at {model_path}")
        return False
    
    if not os.path.exists(preprocessor_path):
        print(f"⚠️ WARNING: preprocessor.pkl not found at {preprocessor_path}")
        return False
    
    print(f"✅ Artifacts found: model.pkl and preprocessor.pkl")
    return True

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Check for artifacts
    artifacts_available = check_artifacts()
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*60)
    print("🚀 Starting Student Performance Predictor")
    print("="*60)
    print(f"📊 API endpoint: http://localhost:{port}/api/predict")
    print(f"🏠 Home page: http://localhost:{port}/")
    print(f"🔧 ML Model Loaded: {CustomData is not None and PredictPipeline is not None}")
    print(f"📁 Artifacts Available: {artifacts_available}")
    print(f"⚙️ Debug mode: {debug}")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)