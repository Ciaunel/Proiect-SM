from flask import Flask, request, jsonify, render_template

app=Flask(__name__)
uStatus="necunoscut" #ultimul status
uDistanta=0 #ultima distanta
uComanda="none" #ultima comanda

@app.route('/')
def home():
    #return "Serverul este activ!"
    return render_template('PicoServer.html',distanta=uDistanta, status=uStatus,comanda=uComanda)

@app.route('/update',methods=['POST'])
def update():
    global uDistanta,uStatus

    data=request.get_json()
    if not data:
        return jsonify(({"error": "JSON invalid sau lipseste"}))
    dist=data.get('distanta')
    state=data.get('status')
    try:
        if dist is not None:
            uDistanta=float(dist)
    except (ValueError, TypeError):
        return jsonify({"error":" eroare la distanta"})
    if state is not None:
        uStatus=state
    print(f"[RECEPTIE] Distanta: {uDistanta} cm | Stare: {uStatus}")
    return jsonify({"raspuns": "ok"})

@app.route('/comanda',methods=['POST'])
def comanda():
    global uComanda
    data=request.get_json()
    if not data or 'act' not in data:
        return jsonify(({"error": "comanda invalida"}))
    cmd=data['act']
    uComanda=cmd
    return jsonify({"status":"trimis","comanda": cmd})

@app.route('/preia_comanda',methods=['GET'])
def preia_comanda():
    return jsonify({"comanda": uComanda})

@app.route('/status')
def status():
    global uDistanta, uStatus, uComanda
    return jsonify({
        "distanta": uDistanta,
        "status": uStatus,
        "comanda": uComanda
    })

if __name__=='__main__':
    app.run(host='192.168.249.19', port=8000)
