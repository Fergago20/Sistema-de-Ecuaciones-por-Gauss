from flask import Flask, jsonify, request, render_template
from controller.logica import Logica

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/generar_campos', methods=['POST'])
def generar_campos():
    data = request.json
    n = data.get('numEcuaciones')
    m = data.get('numIncognitas')

    if not isinstance(n, int) or not isinstance(m, int) or n <= 0 or m <= 0:
        return jsonify({"error": "Número de ecuaciones e incógnitas deben ser enteros positivos."}), 400

    logica = Logica(m, n)
    logica.limpiar()
    inputs = []

    for i in range(n):
        fila_entries = []
        for j in range(m):
            fila_entries.append(f"x{j+1}")
        fila_entries.append("=")
        fila_entries.append("independiente")
        inputs.append(fila_entries)

    return jsonify({"inputs": inputs}), 200

@app.route('/resolver', methods=['POST'])
def resolver():
    data = request.json
    ecuaciones = data.get('ecuaciones')
    numEcuaciones = len(ecuaciones)
    numIncognitas = len(ecuaciones[0]) - 1 if numEcuaciones > 0 else 0

    # 🔑 Convertir a float (y aceptar vacíos como 0)
    try:
        ecuaciones = [[float(valor) if valor != "" else 0.0 for valor in fila] for fila in ecuaciones]
    except ValueError:
        return jsonify({"error": "Todos los coeficientes deben ser números válidos."}), 400

    logica = Logica(numIncognitas, numEcuaciones)

    try:
        for ecuacion in ecuaciones:
            logica.agregar_ecuacion(ecuacion)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    matriz_resuelta = logica.resolver_sistema()
    if isinstance(matriz_resuelta, str):
        return jsonify({"error": matriz_resuelta}), 400
    return jsonify({
        "matriz_resuelta": matriz_resuelta,
        "resultados": matriz_resuelta
    }), 200



if __name__ == '__main__':
    app.run(debug=True)