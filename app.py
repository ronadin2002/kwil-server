from flask import Flask, request, redirect, render_template, session
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = 'Ov23liIMPjBwpHZZ43Xi'  # Replace with your GitHub OAuth App client ID
CLIENT_SECRET = 'a18d5ec32b867ff46811cdd09f98995c972d260a'  # Replace with your GitHub OAuth App client secret

@app.route('/')
def home():
    return 'Home Page'


@app.route('/callback')
def callback():
    print("here")
    code = request.args.get('code')
    token_url = 'https://github.com/login/oauth/access_token'
    token_data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    token_response = requests.post(token_url, data=token_data, headers=headers)
    token_json = token_response.json()
    access_token = token_json.get('access_token')

    # Save the access token in the session
    session['access_token'] = access_token

    return redirect('/repos')

@app.route('/repos')
def repos():
    access_token = session.get('access_token')
    if not access_token:
        return redirect('/')

    # Fetch the user's repositories from GitHub API
    repos_response = requests.get('https://api.github.com/user/repos', headers={
        'Authorization': f'token {access_token}'
    })
    repos = repos_response.json()

    return render_template('repos.html', repos=repos)

@app.route('/repo/<repo_full_name>')
def repo(repo_full_name):
    return f'You selected {repo_full_name}'

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
