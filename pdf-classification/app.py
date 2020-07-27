
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 

Course work: 

@author: FLASK-INTERN-TEAM

Source:
    https://stackoverflow.com/questions/13279399/how-to-obtain-values-of-request-variables-using-python-and-flask
'''
from __future__ import unicode_literals, print_function
from flask import Flask, render_template, request, make_response
from PyPDF2 import PdfFileReader, PdfFileWriter
import requests
import json
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
from werkzeug.utils import secure_filename
import os
import plac
import random
from pathlib import Path
import spacy
from tqdm import tqdm

#from spellchecker import SpellChecker
import re

tech = 'techclassify'
nlp1 = spacy.load(tech)


app = Flask(__name__)


'''
    http://127.0.0.1:5000/show_pdf
'''


@app.route('/', methods=['GET', 'POST'])
def hello():
    return "hello world"


@app.route('/show_pdf', methods=['GET', 'POST'])
def show_pdf():
    UPLOAD_FOLDER = './static/uploads'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    pdf_path = None
    error_msg = None
    pdf = None
    if request.method == 'POST':
        file = request.files['pdf']
        if file.filename == '':
            error_msg = "Please Upload Any PDF"
        else:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            pdf_path = "./static/uploads/{}".format(filename)
            #PDF_file = "python_basics.pdf"
            pages = convert_from_path(pdf_path)
            image_counter = 1
            for page in pages:
                file_name = "page_"+str(image_counter)+".jpg"
                page.save(file_name, 'JPEG')

    # Increment the counter to update filename
                image_counter = image_counter + 1


# Variable to get count of total number of pages
            filelimit = image_counter-1

            outfile = "1.txt"

            f = open(outfile, "a")
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = " "
            for i in range(1, filelimit + 1):
                filename = "page_"+str(i)+".jpg"

                text += str(((pytesseract.image_to_string(Image.open(filename)))))

                text = text.replace('-\n', '')
                f.write(text)
            f.close()
            # rev=request.form['konjactext']
            rev = text
            r = nlp1(rev.lower())

            if rev.lower().find('python') > 0 or rev.lower().find('system') > 0 or rev.lower().find('program') > 0 or rev.lower().find('software') > 0 or rev.lower().find('version') > 0:
                l = [(ent.text, ent.label_, ent.start_char, ent.end_char)
                     for ent in r.ents]
                x = {"file_name": filename,
                     "type": "TECH file"}

                return render_template('show_pdf.html', pdf_path=pdf_path, result=x)
            else:
                y = {"file_name": filename,
                     "type": "Non TECH file"}
                return render_template('show_pdf.html', pdf_path=pdf_path, result=y)

    return render_template("show_pdf.html", pdf_path=pdf_path, error_msg=error_msg)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)
