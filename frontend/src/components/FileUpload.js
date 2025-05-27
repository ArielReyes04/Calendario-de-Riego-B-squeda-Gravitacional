import React, { useState } from 'react';
import './FileUpload.css';

function FileUpload({ setTerrenoFile, setCultivosFile }) {
  const [dragOverTerreno, setDragOverTerreno] = useState(false);
  const [dragOverCultivo, setDragOverCultivo] = useState(false);
  const [fileNameTerreno, setFileNameTerreno] = useState('');
  const [fileNameCultivo, setFileNameCultivo] = useState('');

  const handleDrop = (e, tipo) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (!file || file.type !== 'text/csv') return;

    if (tipo === 'terreno') {
      setTerrenoFile(file);
      setFileNameTerreno(file.name);
      setDragOverTerreno(false);
    } else {
      setCultivosFile(file);
      setFileNameCultivo(file.name);
      setDragOverCultivo(false);
    }
  };

  return (
    <div className="file-upload-container p-4 rounded shadow mb-4">
      <h2 className="h4 mb-4 text-white">📁 Cargar Archivos CSV</h2>
      <div className="row g-4">
        {/* Drop zona terreno */}
        <div className="col-md-6">
          <div
            className={`drop-zone ${dragOverTerreno ? 'drag-over' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setDragOverTerreno(true); }}
            onDragLeave={() => setDragOverTerreno(false)}
            onDrop={(e) => handleDrop(e, 'terreno')}
          >
            <label htmlFor="terrenoFile" className="form-label text-light">Datos del Terreno</label>
            <input
              type="file"
              id="terrenoFile"
              accept=".csv"
              onChange={(e) => {
                setTerrenoFile(e.target.files[0]);
                setFileNameTerreno(e.target.files[0]?.name || '');
              }}
              className="form-control mb-2"
            />
            <div className="drop-text">
              {fileNameTerreno
                ? `Seleccionado: ${fileNameTerreno}`
                : 'Arrastra aquí el archivo CSV del terreno'}
            </div>
          </div>
        </div>

        {/* Drop zona cultivo */}
        <div className="col-md-6">
          <div
            className={`drop-zone ${dragOverCultivo ? 'drag-over' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setDragOverCultivo(true); }}
            onDragLeave={() => setDragOverCultivo(false)}
            onDrop={(e) => handleDrop(e, 'cultivo')}
          >
            <label htmlFor="cultivosFile" className="form-label text-light">Datos de Cultivos</label>
            <input
              type="file"
              id="cultivosFile"
              accept=".csv"
              onChange={(e) => {
                setCultivosFile(e.target.files[0]);
                setFileNameCultivo(e.target.files[0]?.name || '');
              }}
              className="form-control mb-2"
            />
            <div className="drop-text">
              {fileNameCultivo
                ? `Seleccionado: ${fileNameCultivo}`
                : 'Arrastra aquí el archivo CSV de cultivos'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default FileUpload;
