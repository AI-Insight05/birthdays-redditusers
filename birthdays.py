from flask import Flask, request, render_template_string, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
  <title>Birthdays !!!</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #fbc2eb, #a6c1ee);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      margin: 0;
    }
    .form-card {
      background-color: #ffffffcc;
      border-radius: 16px;
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
      padding: 30px;
      width: 300px;
      text-align: center;
    }
    img {
      width: 150px;
      margin-bottom: 20px;
      border-radius: 12px;
    }
    input[type="number"],
    input[type="text"] {
      padding: 10px;
      margin: 10px 0;
      border: none;
      border-radius: 8px;
      width: 100%;
      font-size: 16px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    input[type="submit"] {
      background-color: #7f53ac;
      color: white;
      padding: 10px 20px;
      margin-top: 15px;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      font-size: 16px;
    }
    input[type="submit"]:hover {
      background-color: #5e3d99;
    }
  </style>
</head>
<body>
  <div class="form-card">
    <img src="/static/party.gif" alt="Party GIF">
    <form method="POST" action="/submit">
      <input type="number" name="date" placeholder="Date (1-31)" min="1" max="31" required><br>
      <input type="number" name="month" placeholder="Month (1-12)" min="1" max="12" required><br>
      <input type="text" name="reddit" placeholder="Reddit username" required><br>
      <input type="submit" value="Submit 🎉">
    </form>
  </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/submit', methods=['POST'])
def submit():
    date = request.form.get('date')
    month = request.form.get('month')
    reddit = request.form.get('reddit')

    if not date or not month or not reddit:
        return "Missing data", 400

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    data.append({'date': date, 'month': month, 'reddit': reddit})

    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    return "<h2>🎉 Saved! <a href='/'>Back</a></h2>"

@app.route('/data')
def view_data():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
