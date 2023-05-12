from flask import Flask, render_template, redirect, request, url_for
import csv
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

@app.route("/")
def my_home():
    return render_template('index.html')


@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)

# def file_writer(data):
#     with open('database.txt', mode='a') as database:
#         email = data["email"]
#         subject = data["subject"]
#         message = data["message"]
#         file = database.write(f'\n{email},{subject},{message}')
        
def csv_file_writer(data):
    with open('database.csv', 'a', newline='') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])
        
def send_email(data):
    email = EmailMessage()
    email['from'] = data["email"]
    email['to'] = 'l3shi@uwaterloo.ca'
    email['subject'] = data["subject"]
    email.set_content(data["message"])
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('dunyueshi@gmail.com', 'acsedmadcpdeyhyu')
        smtp.send_message(email)
        
        
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try: 
            data = request.form.to_dict()
            csv_file_writer(data)
            send_email(data)
            return redirect('/thankyou.html')
        except:
            return redirect('/error.html')
    else:
        return 'something wrong'
