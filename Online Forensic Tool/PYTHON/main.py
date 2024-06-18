from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def rt():
    return render_template('ia.html')

if __name__ == '__main__':
    app.run(port=5500, debug=True)