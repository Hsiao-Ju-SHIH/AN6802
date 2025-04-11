from flask import Flask, request, render_template
import sqlite3
import datetime
import google.generativeai as genai
import os
import wikipedia
import requests

api = os.getenv("makersuite")
genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-1.5-flash')

api_image = os.getenv('imagesearch')

app = Flask(__name__)

flag = 1

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/main', methods=['POST', 'GET'])
def main():
    global flag
    if flag == 1:
        user_name = request.form.get('q')
        t = datetime.datetime.now()
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('insert into user (name, timestamp) values (?, ?)', (user_name, t))
        conn.commit()
        c.close()
        conn.close()
        flag = 0
    return render_template('main.html')

@app.route('/foodexp', methods=['POST', 'GET'])
def foodexp():
    return render_template('foodexp.html')

@app.route('/foodexp1', methods=['POST', 'GET'])
def foodexp1():
    return render_template('foodexp1.html')

@app.route('/foodexp2', methods=['POST', 'GET'])
def foodexp2():
    return render_template('foodexp2.html')

@app.route('/foodexp_pred', methods=['POST', 'GET'])
def foodexp_pred():
    q = float(request.form.get('q'))
    return render_template('foodexp_pred.html', r = (q * 0.48517842 + 147.47538852370565))
    
@app.route('/ethical_test', methods=['POST', 'GET'])
def ethical_test():
    return render_template('ethical_test.html')

@app.route('/FAQ', methods=['POST', 'GET'])
def FAQ():
    return render_template('FAQ.html')

@app.route('/FAQ1', methods=['POST', 'GET'])
def FAQ1():
    r = model.generate_content('What are the key drivers of a company’s profitability')
    return render_template('FAQ1.html', r=r.candidates[0].content.parts[0].text)

@app.route('/FAQinput', methods=['POST', 'GET'])
def FAQinput():
    q = request.form.get("q")
    r = wikipedia.summary(q)
    return render_template('FAQinput.html', r=r)

@app.route('/altInvest', methods=['POST', 'GET'])
def altInvest():
    # api = 'AIzaSyDar1zTonZY1Z-8k56SYkxKcED2YRt6eO0'
    id = '32dd497be354f4627'
    q = r'painting%20for%20sale'
    num = 5
    url = f'https://www.googleapis.com/customsearch/v1?key={api_image}&cx={id}&q={q}&searchType=image&num={num}'
    res = requests.get(url=url)
    res_json = res.json()
    urls = [res_json['items'][i]['link'] for i in range(len(res_json['items']))]
    r = urls[0]
    return render_template('altInvest.html', r=r)

@app.route('/userLog', methods=['POST', 'GET'])
def userLog():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('select * from user')
    r = ''
    for row in c:
        print(row)
        r += str(row) + '\n'
    c.close()
    conn.close()
    return render_template('userLog.html', r=r)

@app.route('/deleteLog', methods=['POST', 'GET'])
def deleteLog():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute('delete from user')
    conn.commit()
    c.close()
    conn.close()
    return render_template('deleteLog.html')


@app.route('/test_result', methods=['POST', 'GET'])
def test_result():
    answer = request.form.get('answer')
    if answer == 'False':
        return render_template('pass.html')
    elif answer == 'True':
        return render_template('fail.html')        

if __name__ == '__main__':
    app.run()