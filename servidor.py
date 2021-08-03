from flask import Flask


PORT = 8080
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main(*args, **kwargs):
    return " Bienvenido mmv"


if __name__ == '__main__':
    app.run('0.0.0.0', port=PORT)