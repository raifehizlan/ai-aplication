# Import Flask modules
from flask import Flask, request, render_template
from flaskext.mysql import MySQL
from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModel
import torch
from typing import Dict, List
from pydantic import BaseModel
from aimped.nlp.pipeline import Pipeline
from aimped.nlp.tokenizer import sentence_tokenizer, word_tokenizer
from huggingface_hub import login
import os
from flask_cors import CORS
import json
# Create an object named app
app = Flask(__name__)
CORS(app) # Tüm kaynaklara erişim izni sağlar

# Configure mysql database
app.config['MYSQL_DATABASE_HOST'] = "deid_db"
app.config['MYSQL_DATABASE_PASSWORD'] = "123"
app.config['MYSQL_DATABASE_DB'] = "deid"
app.config['MYSQL_DATABASE_USER'] = "raife"
project_db = "deid"
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app) 
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()

# Load model
#login(token = token)
#tokenizer = AutoTokenizer.from_pretrained("Hizlan/ner_pii", use_auth_token=True)
#model = AutoModelForTokenClassification.from_pretrained("Hizlan/ner_pii", use_auth_token=True)
#device = "cuda" if torch.cuda.is_available() else "cpu"
#model = model.to(device)
#ner_pipeline = Pipeline(model=model, tokenizer=tokenizer, device=device)

# Load model directly

# Load model directly

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER-uncased")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER-uncased")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
ner_pipeline = Pipeline(model=model, tokenizer=tokenizer, device=device)



def make_prediction(ner_pipeline, text):
    #white_label_list = ['AGE', 'CITY', 'COUNTRY', 'DATE', 'IDNUM', 'NAME', 'ORGANIZATION', 'PHONE', 'PROFESSION', 'STREET', 'ZIP', 'EMAIL', 'URL','SSN','IP','ACCOUNT', 'STATE', 'FAX']
    white_label_list = ['MISC', 'PER', 'ORG', 'LOC']

    sentences = sentence_tokenizer(text, language='english')
    sents_tokens_list = word_tokenizer(sentences)
    tokens, preds, probs, begins, ends = ner_pipeline.ner_result(text=text,
                                                                sents_tokens_list=sents_tokens_list,
                                                                sentences=sentences)
    results = ner_pipeline.chunker_result(text, white_label_list, tokens, preds, probs, begins, ends)
    regex_json_files_path = "json"
    results = ner_pipeline.regex_model_output_merger(regex_json_files_path, results, text, white_label_list)
    results = ner_pipeline.deid_result(text, results,fake_csv_path='', faked=False, masked=True)
    return results['masked_text']


def init_deid_db():
    deid_table = """
    CREATE TABLE IF NOT EXISTS """+ project_db +""".deid(
    id INT NOT NULL AUTO_INCREMENT,
    data TEXT NOT NULL,
    result TEXT NOT NULL,
    PRIMARY KEY (id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    cursor.execute(deid_table)



def insert_data(data, result):

    insert = f"""
    INSERT INTO deid (data, result)
    VALUES ('{data.strip()}', '{result.strip()}');
    """
    cursor.execute(insert)
    result = cursor.fetchall()
    print('data and result was inserted to database successfully')


# Write a function named `add_record` which inserts new record to the database using `GET` and `POST` methods,
# using template files named `add-update.html` given under `templates` folder
# and assign to the static route of ('add')
@app.route('/prediction', methods=['POST'])
def add_record():
    print('basladik')
    text = request.form['data']
    print('datayi aldik', text)
    result = make_prediction(ner_pipeline, text)
    print('prediction oldu' , result)
    insert_data(text, result)
    return json.dumps({"result": result})




# Add a statement to run the Flask application which can be reached from any host on port 80.
if __name__== '__main__':
    init_deid_db()
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5000) 
