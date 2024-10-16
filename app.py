import os
import pandas as pd
from flask import Flask, request, render_template
import openai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Set your OpenAI API key here
openai.api_key = 'xxx'

def analyze_data(df, question):
    # Convert DataFrame to a string representation for ChatGPT
    data_str = df.to_string()
    prompt = f"You are an AI data analyst. Here is the data:\n{data_str}\n\nQuestion: {question}"
    
    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response['choices'][0]['message']['content']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyzer')
def analyzer():
    return render_template('upload.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Read the Excel file
        df = pd.read_excel(filepath)
        
        # Get user question
        question = request.form['question']
        
        # Analyze data and get response from ChatGPT
        response = analyze_data(df, question)
        
        return f"<h3>Response:</h3><p>{response}</p>"

if __name__ == '__main__':
    app.run(debug=True)

