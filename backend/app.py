# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from optimizer import run_gsa
import pandas as pd

app = Flask(__name__)
CORS(app)  # Habilita CORS

@app.route('/api/run-gsa', methods=['POST'])
def run_gsa_endpoint():
    try:
        # Verificar que se enviaron los archivos CSV
        if 'terreno' not in request.files or 'cultivos' not in request.files:
            return jsonify({"error": "Faltan archivos CSV (terreno o cultivos)"}), 400

        terreno_file = request.files['terreno']
        cultivos_file = request.files['cultivos']

        # Leer CSVs
        try:
            datos_terreno = pd.read_csv(terreno_file)
            datos_cultivos = pd.read_csv(cultivos_file)
        except Exception as e:
            return jsonify({"error": f"Error al leer CSVs: {str(e)}"}), 400

        # Obtener parámetros
        tamano_poblacion = int(request.form.get('tamano_poblacion', 50))
        iteraciones = int(request.form.get('iteraciones', 200))

        # Ejecutar GSA
        resultado = run_gsa(datos_terreno, datos_cultivos, tamano_poblacion, iteraciones)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({"error": f"Error en el servidor: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
