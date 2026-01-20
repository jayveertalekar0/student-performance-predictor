from flask import Flask, request, render_template, jsonify
import os
import sys
import traceback

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.pipeline.predict_pipeline import CustomData, PredictPipeline
except ImportError as e:
    print(f"Warning: Could not import ML modules: {e}")

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
        pipeline = PredictPipeline()
        result = pipeline.predict(df)[0]
        
        # Ensure result is within bounds
        result = max(0, min(100, float(result)))
        
        # Store prediction
        predictions.append({
            'score': round(float(result), 1),
            'category': get_category(float(result))
        })
        
        # Keep only last 20 predictions
        if len(predictions) > 20:
            predictions.pop(0)
        
        return render_template('predict.html', 
                             result=round(float(result), 1),
                             category=get_category(float(result)))
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"Prediction error: {error_msg}")
        print(traceback.format_exc())
        return render_template('predict.html', error=error_msg)

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
        
        # Create data object
        custom_data = CustomData(
            gender=data['gender'],
            race_ethnicity=data['race_ethnicity'],
            parental_level_of_education=data['parental_level_of_education'],
            lunch=data['lunch'],
            test_preparation_course=data['test_preparation_course'],
            reading_score=float(data['reading_score']),
            writing_score=float(data['writing_score'])
        )
        
        # Get prediction
        df = custom_data.get_data_as_data_frame()
        pipeline = PredictPipeline()
        result = pipeline.predict(df)[0]
        result = max(0, min(100, float(result)))
        category = get_category(result)
        
        # Store prediction
        predictions.append({
            'score': round(float(result), 1),
            'category': category
        })
        
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
            'timestamp': len(predictions)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for deployment"""
    return jsonify({
        'status': 'healthy',
        'predictions_count': len(predictions),
        'service': 'student-performance-predictor'
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

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting Student Performance Predictor on port {port}")
    print(f"📊 API endpoint: http://localhost:{port}/api/predict")
    print(f"🏠 Home page: http://localhost:{port}/")
    
    app.run(host='0.0.0.0', port=port, debug=debug)