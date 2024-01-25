from flask import Flask, render_template
import requests, random

app = Flask(__name__)
API_URL = 'https://cat-fact.herokuapp.com/facts'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/fact-table', methods=['GET', 'POST'])
def get_facts():
    try:
        response = requests.get(API_URL)
        response.raise_for_status() #checking for HTTP errors
        facts = response.json()
        fact_list = []
        
        for fact in facts:
            if fact['status']['verified']: #filtering verified facts
                fact_list.append([fact['text'], fact['type']])

        curr_fact, curr_type = random.choice(fact_list) #selecting random fact from the list of facts

        return render_template('fact.html', fact_text=curr_fact, fact_type=curr_type)
    
    except requests.exceptions.RequestException as e: #handling HTTP errors
        error_msg = 'Error fetching data: ' + str(e)

        return render_template('error.html', error_msg=error_msg)

    except Exception as e: #handling other errors
        error_msg = 'Unexpected error occurred: ' + str(e)

        return render_template('error.html', error_msg=error_msg)
    
@app.errorhandler(404)
def page_not_found(error):
    error_msg = 'Page not found'

    return render_template('error.html', error_msg=error_msg)

if __name__ == '__main__':
    app.run(debug=True) 