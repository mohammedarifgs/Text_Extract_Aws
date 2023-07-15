from flask import Flask, request, render_template,redirect
import boto3
import json
import csv


textractclient = boto3.client("textract", aws_access_key_id="AKIASODT36CXC2DG3PWR",
                              aws_secret_access_key="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", region_name="us-east-1")


app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html", jsonData=json.dumps({}))




@app.route("/<string:page_name>")
def html_page(page_name):
    return render_template(page_name)


@app.route("/extract", methods=["POST"])
def extractImage():

    file = request.files.get("filename")
    binaryFile = file.read()
    response = textractclient.detect_document_text(
        Document={
            'Bytes': binaryFile
        }
    )

    extractedText = ""

    for block in response['Blocks']:
        if block["BlockType"] == "LINE":
             #print('\033[94m' + item["Text"] + '\033[0m')
             extractedText = extractedText+block["Text"]+" "

    responseJson = {

        "text": extractedText
    }
    print(responseJson)
    return render_template("works.html", jsonData=json.dumps(responseJson))

def write_to_csv(data):
    with open('database12.csv',newline='',mode='a') as database:
        email=data["email"]
        subject=data["subject"]
        message=data["feedback"]
        csv_writer=csv.writer(database, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method =='POST':
        data=request.form.to_dict()
        write_to_csv(data)
        print(data)
        return redirect('/thankyou.html')


app.run()
