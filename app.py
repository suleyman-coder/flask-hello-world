import requests
from flask import Flask, request, Response


app = Flask(__name__)

# ==========================================================
# dostum burada
# ==========================================================

VPS_ADDRESS = "http://135.148.82.236"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    vps_url = f"{VPS_ADDRESS}/{path}"


    headers = {key: value for (key, value) in request.headers if key.lower() != 'host'}
    

    try:
        resp = requests.request(
            method=request.method,
            url=vps_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            params=request.args,
            stream=True
        )
    except requests.exceptions.RequestException as e:
        print(f"VPS-e birikme ýalňyşlygy: {e}")
        return "Serwer ýalňyşlygy: Aralyk serwere birikip bolmady.", 502


    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                        if name.lower() not in excluded_headers]

    response = Response(resp.iter_content(chunk_size=1024), resp.status_code, response_headers)
    
    return response

if __name__ == '__main__':

    try:
        app.run(host='0.0.0.0', port=80, debug=True)
    except OSError as e:
        if e.errno == 13 or e.errno == 10013:
            print("\n**** ÝALŇYŞLYK: Port 80-i ulanmak üçin 'sudo' bilen işlediň. ****")
            print("**** Buýruk: sudo python your_script_name.py ****\n")
