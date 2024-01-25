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

def dfs(node, deleted, res):
    if not node:
        return node
    
    node.left = dfs(node.left, deleted, res)
    node.right = dfs(node.right, deleted, res)

    if node.val in deleted:
        if node.left:
            res.append(node.left)
        if node.right:
            res.append(node.right)

        return None
    
    return node

from collections import defaultdict
def subarrays(nums):
    res = 0
    d = defaultdict(int)
    left = 0

    for right in range(len(nums)):
        d[nums[right]] += 1

        while max(d) - min(d) > 2:
            d[nums[left]] -= 1
            if d[nums[left]] == 0:
                del d[nums[left]]
            left += 1

        res += right - left + 1

    return res

def get_max(nums):
    return max(nums)

if __name__ == '__main__':
    app.run(debug=True) 
