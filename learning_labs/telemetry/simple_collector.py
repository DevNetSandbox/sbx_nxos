from flask import Flask, request

# Initialize the Flask application
app = Flask(__name__)

@app.route('/<path:path>', methods = ['POST'])
def collect(path):
    try:
        fh = open ('/tmp/nxos.log', 'a')
        fh.write(request.data)
        print(request.data)
        fh.write("\n\n")
    except KeyboardInterrupt:
        fh.close()
    return ''


# Run
if __name__ == '__main__':
    with open('/tmp/nxos.log', 'w') as fh:
        fh.write("Initializing log....\n\n")
        
    app.run(host='0.0.0.0', port=8888,  debug=True)
    
