import React, { useState } from 'react';
import GSASettings from './components/GSASettings';
import FileUpload from './components/FileUpload';
import ResultsDisplay from './components/ResultsDisplay';
import axios from 'axios';
import { Loader, AlertCircle } from 'lucide-react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'; // Aquí irá el estilo personalizado

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tamanoPoblacion, setTamanoPoblacion] = useState(50);
  const [iteraciones, setIteraciones] = useState(200);
  const [terrenoFile, setTerrenoFile] = useState(null);
  const [cultivosFile, setCultivosFile] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!terrenoFile || !cultivosFile) {
      setError('Por favor, seleccione ambos archivos CSV.');
      return;
    }

    setLoading(true);
    setError(null);
    setResults(null);

    const formData = new FormData();
    formData.append('terreno', terrenoFile);
    formData.append('cultivos', cultivosFile);
    formData.append('tamano_poblacion', tamanoPoblacion);
    formData.append('iteraciones', iteraciones);

    try {
      const response = await axios.post('http://localhost:5000/api/run-gsa', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      if (response.data.status === 'success') {
        setResults(response.data);
      } else {
        setError(response.data.error);
      }
    } catch (err) {
      setError('Error al conectar con el servidor. Asegúrese de que el backend esté ejecutándose.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container d-flex align-items-center justify-content-center min-vh-100 bg-dark text-white px-3">
      <div className="card custom-card shadow-lg p-4 w-100" style={{ maxWidth: '800px' }}>
        <h1 className="text-center mb-4">🌾 Optimización Agrícola con GSA</h1>
        <form onSubmit={handleSubmit}>
          <GSASettings
            tamanoPoblacion={tamanoPoblacion}
            setTamanoPoblacion={setTamanoPoblacion}
            iteraciones={iteraciones}
            setIteraciones={setIteraciones}
          />
          <FileUpload
            setTerrenoFile={setTerrenoFile}
            setCultivosFile={setCultivosFile}
          />
          <button type="submit" className="btn btn-success w-100 mt-3">
            Ejecutar GSA
          </button>
        </form>

        {loading && (
          <div className="text-center mt-4 text-info d-flex justify-content-center align-items-center">
            <Loader className="me-2 spinner-border spinner-border-sm" /> Procesando...
          </div>
        )}

        {error && (
          <div className="alert alert-danger mt-4 d-flex align-items-center justify-content-center">
            <AlertCircle className="me-2" /> {error}
          </div>
        )}

        {results && (
          <div className="mt-5">
            <ResultsDisplay results={results} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
