from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

@app.route("/contact/")
def moncontact():
     return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique2():
    return render_template("graphique2.html")

# Route pour obtenir les commits
@app.route('/commits/')
def commits():
    # URL de l'API GitHub pour les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Compter les commits par minute
    commit_count = {}
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        date_object = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.strftime('%Y-%m-%d %H:%M')
        if minute in commit_count:
            commit_count[minute] += 1
        else:
            commit_count[minute] = 1

    # Trier les données par minute
    minutes = sorted(commit_count.keys())
    counts = [commit_count[minute] for minute in minutes]

    # Générer le graphique
    fig, ax = plt.subplots()
    ax.bar(minutes, counts)
    ax.set_xlabel('Minute')
    ax.set_ylabel('Nombre de Commits')
    ax.set_title('Nombre de Commits par Minute')

    # Sauvegarder le graphique dans un buffer et le convertir en base64
    buf = io.BytesIO()
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    # Afficher le graphique dans une page HTML
    return render_template('commits.html', image_base64=image_base64)


  
if __name__ == "__main__":
  app.run(debug=True)
