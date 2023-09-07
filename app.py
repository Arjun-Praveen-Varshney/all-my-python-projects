from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
#from analyze import analyze_resume
import logging
import sys
import pdfplumber
import openai
import json
#from dotenv import load_dotenv
# from memory_profiler import profile

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


app = Flask(__name__)

CORS(app)  # This will enable CORS for all routes

app.config['UPLOAD_FOLDER'] = '/home/uploads/'
UPLOAD_FOLDER = '/home/uploads/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        resume = request.files.get('resume')
        job_description = request.files.get('job_description')
        if resume and job_description:
            resume_filename = secure_filename(resume.filename)
            job_description_filename = secure_filename(job_description.filename)
            resume.save(os.path.join(app.config['UPLOAD_FOLDER'], resume_filename))
            job_description.save(os.path.join(app.config['UPLOAD_FOLDER'], job_description_filename))
            return redirect(url_for('analyze_files', resume_filename=resume_filename, job_description_filename=job_description_filename))
    return render_template('upload.html')


@app.route('/analyze/<resume_filename>/<job_description_filename>')
def analyze_files(resume_filename, job_description_filename):
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_filename)
    job_description_path = os.path.join(app.config['UPLOAD_FOLDER'], job_description_filename)
    results = analyze_resume(resume_path, job_description_path)
    #print(results)
    return render_template('result.html', results=results)


def read_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = " ".join(page.extract_text() for page in pdf.pages)
    return text



#load_dotenv()

def classify_resume(text):
    prompt=f"Based on the following text, determine if it's a resume or not. If it's not a resume, \
               return a message saying 'We think this is not a resume, are you sure you uploaded a resume or a CV?'\n\n{text}"
    
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "You are a resume classificaiton assistant. You either reply with 'resume' or 'not resume', \
                                       to-the-point answers with no elaboration."},
        {"role": "user", "content": prompt},
      ],
      temperature=0,
      max_tokens=20
    )
    return response["choices"][0]["message"]["content"]


def extract_personal_info(text):
    prompt = f"From the following resume, extract the personal information of the candidate in a structured JSON format.\n\n{text}"
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "You are a personal information extraction assistant. \
                                       Extract the information in a structured JSON format. The JSON structure should be as follows: \
                                       {'Name': '', 'Contact Information': {'Email': '', 'Phone': '', 'Address': '', 'LinkedIn': ''}, 'Summary': ''}"},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": '{"Name": "", "Contact Information": {"Email": "null", "Phone": "null", "Address": "null", "LinkedIn": "null"}, "Summary": "null"}'},
      ],
      temperature=0,
      max_tokens=1000
    )
    return response["choices"][0]["message"]["content"]


def generate_job_description(job_title, experience_level):
    try:
        # Construct a prompt for OpenAI
        prompt = f"Generate a job description for the position of {job_title}. The desired experience level is {experience_level}. Assume the required skills, responsibilities, and qualifications based on the job title and experience level."

        # Get the response from OpenAI
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=[
            {"role": "system", "content": "You are a job description generation assistant. Provide a professional and detailed job description based on the provided job title and experience level. Assume the required skills, responsibilities, and qualifications appropriate for the role."},
            {"role": "user", "content": prompt},
          ],
          temperature=0.5,
          max_tokens=1000
        )

        job_description_text = response["choices"][0]["message"]["content"]
        return job_description_text
        # return jsonify({'job_description': job_description_text})

    except Exception as e:
        logging.error(f"An error occurred in generate_job_description: {e}")
        return jsonify({'error': str(e)}), 500

def score_and_feedback(resume_text, job_description_text):
    prompt = f"The candidate's resume contains the following information:\n{resume_text}\nThe job description for the position they're applying for is as follows:\n{job_description_text}\nFirst, provide a score out of 10 for how well the resume matches the job description. Then, provide detailed feedback on what's missing and what could be improved in the resume based on this score."
    
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {"role": "system", "content": "You are a career advisor and your task is to first provide a score out of 10 based on how well the resume matches the job description. Then, provide detailed, constructive feedback on the candidate's resume, pointing out the areas where the resume matches the job description and where it falls short. Also, suggest improvements that could make the resume better aligned with the job description. Please provide the score and feedback in a structured JSON format."},
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": '{"score": 7, "feedback": "The candidate has a strong background in... However, they could improve their resume by..."}'},  # The assistant's response will be generated by the OpenAI API.
      ],
      temperature=0.5,
      max_tokens=1000
    )
    return response["choices"][0]["message"]["content"]


@app.route('/api/analyze', methods=['POST'])
def analyze_api():
    try:
        #logging.info("Received request in /api/analyze")
        job_description = None
        job_description_path = None
        # Check if the post request has the file part
        if 'resume' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        if 'job_description' in request.files:
            job_description = request.files['job_description']
            job_description_path = os.path.join(UPLOAD_FOLDER, secure_filename(job_description.filename))
            job_description.save(job_description_path)
            job_description_text = read_pdf(job_description_path)
        else:
            try:
              job_title = request.form.get('job_title', '')
              experience_level = request.form.get('experience_level', '')
            except Exception as e:
              #logging.error(f"An error occurred in /api/analyze: {e}")
              return jsonify({'error': str(e)}), 500
            job_description_text = generate_job_description(job_title, experience_level)
        
        resume = request.files['resume']
        resume_path = os.path.join(UPLOAD_FOLDER, secure_filename(resume.filename))
        resume.save(resume_path)

        # If it doesn't exist, extract text from PDF
        resume_text = read_pdf(resume_path)

        # Classify the document
        classification = classify_resume(resume_text)

        # If the document is not a resume, return a message
        if classification != "resume":
            return "We think this is not a resume, are you sure you uploaded a resume or a CV?"

        # Extract personal info, skills, experience, extra info, and publications
        personal_info_response = extract_personal_info(resume_text)
      
        # Construct the result as a dictionary
        results = {
            'personal_info': personal_info_response, 
        }

        score_response = score_and_feedback(resume_text, job_description_text)
        results['score'] = score_response
        return results
        #logging.info(f"analyze_resume returned: {results}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise


if __name__ == '__main__':
    app.run(debug=False)
