import React, { useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function ResultsDisplay({ results }) {
  const { estrategia_optima, curva_convergencia, grafico_convergencia } = results;
  const [fechaInicioReal, setFechaInicioReal] = useState('');
  const [calendario, setCalendario] = useState([]);
  const [mesCalendario, setMesCalendario] = useState(null);
  const [anioCalendario, setAnioCalendario] = useState(null);
  const [diaSeleccionado, setDiaSeleccionado] = useState(null);

  const chartData = {
    labels: curva_convergencia.map((_, index) => index + 1),
    datasets: [
      {
        label: 'Ganancia Neta ($)',
        data: curva_convergencia,
        borderColor: '#4fc3f7',
        backgroundColor: 'rgba(79, 195, 247, 0.2)',
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top', labels: { color: '#ccc' } },
      title: {
        display: true,
        text: 'Curva de Convergencia del GSA',
        color: '#fff',
        font: { size: 18 },
      },
    },
    scales: {
      x: { title: { display: true, text: 'Iteración', color: '#ccc' }, ticks: { color: '#ccc' } },
      y: { title: { display: true, text: 'Ganancia Neta ($)', color: '#ccc' }, ticks: { color: '#ccc' } },
    },
  };

  const generarCalendario = () => {
    if (!fechaInicioReal) return;

    const fechaBase = new Date(fechaInicioReal);
    fechaBase.setDate(fechaBase.getDate() + 1);
    const calendarioGenerado = estrategia_optima.programa_riego_mm_cada_10_dias.map((riego, index) => {
      const fecha = new Date(fechaBase);
      fecha.setDate(fecha.getDate() + index * 10);

      return {
        dia: index + 1,
        fechaObj: fecha,
        fecha: fecha.toISOString().split('T')[0],
        riego: riego.toFixed(2),
        abono: estrategia_optima.dosis_abono_organico_kg_ha_cada_10_dias[index]?.toFixed(2) || "0.00"
      };
    });

    setCalendario(calendarioGenerado);
    if (calendarioGenerado.length > 0) {
      setMesCalendario(calendarioGenerado[0].fechaObj.getMonth());
      setAnioCalendario(calendarioGenerado[0].fechaObj.getFullYear());
    }
  };

  const calcularFechaCosecha = () => {
    if (!fechaInicioReal) return '';
    const inicio = new Date(fechaInicioReal);
    const diasCosecha = estrategia_optima.fecha_cosecha - estrategia_optima.fecha_siembra;
    const fechaCosecha = new Date(inicio);
    fechaCosecha.setDate(inicio.getDate() + diasCosecha);
    return fechaCosecha.toISOString().split('T')[0];
  };

  const fechaSiembra = fechaInicioReal ? new Date(fechaInicioReal) : null;
  if (fechaSiembra) fechaSiembra.setDate(fechaSiembra.getDate() + 1);

  const fechaCosecha = fechaInicioReal
    ? new Date(new Date(fechaInicioReal).setDate(
        new Date(fechaInicioReal).getDate() +
        (estrategia_optima.fecha_cosecha - estrategia_optima.fecha_siembra)
      ))
    : null;

  const obtenerMesCalendario = () => {
    if (mesCalendario === null || anioCalendario === null) return [];

    const primerDiaMes = new Date(anioCalendario, mesCalendario, 1);
    const ultimoDiaMes = new Date(anioCalendario, mesCalendario + 1, 0);
    const totalDias = ultimoDiaMes.getDate();

    const semanas = [];
    let semana = [];
    let diaSemana = primerDiaMes.getDay();

    for (let i = 0; i < diaSemana; i++) semana.push(null);

    for (let dia = 1; dia <= totalDias; dia++) {
      const fechaActual = new Date(anioCalendario, mesCalendario, dia);
      const evento = calendario.find(e =>
        e.fechaObj.getFullYear() === fechaActual.getFullYear() &&
        e.fechaObj.getMonth() === fechaActual.getMonth() &&
        e.fechaObj.getDate() === fechaActual.getDate()
      );
      semana.push(evento || { fechaObj: fechaActual, dia, riego: null, abono: null });

      if (semana.length === 7) {
        semanas.push(semana);
        semana = [];
      }
    }

    while (semana.length > 0 && semana.length < 7) semana.push(null);
    if (semana.length > 0) semanas.push(semana);

    return semanas;
  };

  const semanasCalendario = obtenerMesCalendario();

  const nombreMeses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];

  const avanzarMes = () => {
    if (mesCalendario === 11) {
      setMesCalendario(0);
      setAnioCalendario(anioCalendario + 1);
    } else {
      setMesCalendario(mesCalendario + 1);
    }
  };

  const retrocederMes = () => {
    if (mesCalendario === 0) {
      setMesCalendario(11);
      setAnioCalendario(anioCalendario - 1);
    } else {
      setMesCalendario(mesCalendario - 1);
    }
  };

  const esFecha = (f1, f2) =>
    f1 && f2 &&
    f1.getFullYear() === f2.getFullYear() &&
    f1.getMonth() === f2.getMonth() &&
    f1.getDate() === f2.getDate();

  return (
    <div className="bg-dark text-light p-4 rounded shadow-lg">
      <div className="mb-4">
        <h5 className="text-info">📅 Selecciona la fecha real de siembra:</h5>
        <div className="d-flex align-items-center gap-2">
          <input
            type="date"
            className="form-control bg-secondary text-light border-0"
            value={fechaInicioReal}
            onChange={(e) => setFechaInicioReal(e.target.value)}
          />
          <button className="btn btn-info" onClick={generarCalendario}>
            Generar Calendario
          </button>
        </div>
      </div>

      {calendario.length > 0 && (
        <div className="mb-4">
          <h5 className="text-success">🗓️ Calendario de Riego y Abono</h5>

          <div className="d-flex justify-content-between align-items-center mb-2">
            <button className="btn btn-outline-light btn-sm" onClick={retrocederMes}>←</button>
            <strong>{nombreMeses[mesCalendario]} {anioCalendario}</strong>
            <button className="btn btn-outline-light btn-sm" onClick={avanzarMes}>→</button>
          </div>

          <table className="table table-dark table-bordered text-center">
            <thead>
              <tr>
                <th>D</th><th>L</th><th>M</th><th>M</th><th>J</th><th>V</th><th>S</th>
              </tr>
            </thead>
            <tbody>
              {semanasCalendario.map((semana, i) => (
                <tr key={i}>
                  {semana.map((dia, idx) => {
                    const bgColor = dia
                      ? esFecha(dia.fechaObj, fechaSiembra)
                        ? '#6c757d'
                        : esFecha(dia.fechaObj, fechaCosecha)
                        ? '#5a6268'
                        : dia.riego
                        ? '#198754'
                        : 'transparent'
                      : 'transparent';

                    const icono = esFecha(dia?.fechaObj, fechaSiembra)
                      ? '🌱'
                      : esFecha(dia?.fechaObj, fechaCosecha)
                      ? '🌾'
                      : '';

                    return (
                      <td
                        key={idx}
                        style={{
                          backgroundColor: bgColor,
                          cursor: dia && dia.riego ? 'pointer' : 'default',
                          verticalAlign: 'top',
                          height: '80px',
                          width: '14%',
                          color: 'white',
                        }}
                        onClick={() => dia && dia.riego && setDiaSeleccionado(dia)}
                      >
                        {dia ? (
                          <>
                            <div><strong>{dia.dia || dia.fechaObj.getDate()} {icono}</strong></div>
                            {dia.riego && <div style={{ fontSize: '0.8em' }}>💧 {dia.riego} mm</div>}
                            {dia.abono && <div style={{ fontSize: '0.8em' }}>🌿 {dia.abono} kg/ha</div>}
                          </>
                        ) : null}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>

          {diaSeleccionado && (
            <div className="alert alert-info mt-3" role="alert">
              <h6>📅 Día {diaSeleccionado.dia || diaSeleccionado.fechaObj.getDate()}</h6>
              <p><strong>Fecha:</strong> {diaSeleccionado.fecha}</p>
              <p><strong>💧 Riego:</strong> {diaSeleccionado.riego} mm</p>
              <p><strong>🌿 Abono:</strong> {diaSeleccionado.abono} kg/ha</p>
              <button className="btn btn-sm btn-outline-light" onClick={() => setDiaSeleccionado(null)}>Cerrar</button>
            </div>
          )}

          <p><strong>🌾 Fecha Estimada de Cosecha:</strong> {calcularFechaCosecha()}</p>
        </div>
      )}

      <div className="mb-5">
        <h3 className="h5 mb-3 text-primary">📈 Gráfica de Convergencia</h3>
        <div className="bg-secondary p-3 rounded">
          <Line data={chartData} options={chartOptions} />
        </div>
      </div>

      <img src={grafico_convergencia} alt="Gráfica de Convergencia" className="img-fluid rounded border border-info" />
    </div>
  );
}

export default ResultsDisplay;
