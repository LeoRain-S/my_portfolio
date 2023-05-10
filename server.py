from flask import Flask, render_template, redirect, request, url_for
import csv
import smtplib



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
    sender = "<l3shi@uwaterloo.ca>"
    receiver = "<dunyueshi@gmail.com>"
    message = f"""\
    Subject: Hi Mailtrap
    To: {receiver}
    From: {sender}

    This is a test e-mail message."""
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        server.login("abc36d454627eb", "3d1aacd2570a65")
        server.sendmail(sender, receiver, message)
        
@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try: 
            data = request.form.to_dict()
            csv_file_writer(data)
            send_email(data)
            return redirect('/thankyou.html')
        except:
            return 'did not save to the database'
    else:
        return 'something wrong'
