from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask('app')


def Convert(string):
    li = list(string.split(" "))
    return li

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/getdrug', methods=["POST"])
def getdrug():

    # get the best drug
    age = request.form.get("age", type=int)
    disease = request.form.get("disease")
    url = "https://disease-drug-matching.p.rapidapi.com/get_drug/" + disease.replace(" ","%20")
    headers = {
    'x-rapidapi-key': "c29ef0829emsh071a716792d5aaep1934a3jsn77d175bb3aeb",
    'x-rapidapi-host': "disease-drug-matching.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    
    drugs = response.json()

    # Check for allergies and stuff

    if drugs[0]['drug'] not in Convert(request.form.get("avoid")):
        drug = drugs[0]['drug']
    elif drugs[1]['drug'] not in Convert(request.form.get("avoid")):
        drug = drugs[1]['drug']
    else:
        return "Patient is allergic to both drugs"

    # fetch dosage


    url=f"https://www.drugs.com/dosage/{drug}.html"
    page=requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    if age > 17:
        titles = soup.find('h2', text = "Usual Adult Dose for "+ disease)
        for item in soup.find_all("p"):
            if not "doses" in item.text:
                pass
            else:
                dose = item
    else:
        titles = soup.find('h2', text = "Usual Pediatric Dose for "+ disease)
        for item in soup.find_all("p"):
            if not "doses" in item.text:
                pass
            else:
                dose = item
    return render_template("index.html", dosage=dose, title=titles)
        
    

app.run(host='0.0.0.0', port=8080)