// components/GSASettings.js
import React from 'react';
import './GSASettings.css'; // Importamos un archivo CSS con los estilos oscuros

function GSASettings({ tamanoPoblacion, setTamanoPoblacion, iteraciones, setIteraciones }) {
  return (
    <div className="gsa-settings-container mb-4 p-4 rounded shadow">
      <h2 className="h4 mb-3">⚙️ Configuración del GSA</h2>
      <div className="row">
        <div className="col-md-6 mb-3">
          <label htmlFor="tamanoPoblacion" className="form-label">Tamaño de Población</label>
          <input
            type="number"
            id="tamanoPoblacion"
            className="form-control custom-input"
            value={tamanoPoblacion}
            onChange={(e) => setTamanoPoblacion(Number(e.target.value))}
            min="10"
          />
        </div>
        <div className="col-md-6 mb-3">
          <label htmlFor="iteraciones" className="form-label">Iteraciones</label>
          <input
            type="number"
            id="iteraciones"
            className="form-control custom-input"
            value={iteraciones}
            onChange={(e) => setIteraciones(Number(e.target.value))}
            min="100"
          />
        </div>
      </div>
    </div>
  );
}

export default GSASettings;
