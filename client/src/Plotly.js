import React from 'react';
import Plot from 'react-plotly.js';

function PlotlyComponent({ data }) {
  let config = { responsive: true };

  const updateChart = (data) => {
    document.querySelector('#last-price').classList.remove('animate__fadeIn');
    let trace_price = {
      x: [data.index.map((t) => new Date(t))],
      y: [data.price],
    };
    let trace_volumes = {
      x: [data.index.map((t) => new Date(t))],
      y: [data.volumes],
    };

    Plot.update('chart', trace_price, {}, 0);
    Plot.update('chart', trace_volumes, {}, 1);
    document.querySelector('#last-price').classList.add('animate__fadeIn');
  };

  return (
    <div>
      <Plot
        data={[
          {
            x: data.index,
            y: data.price,
            z: data.volume,
            type: 'scatter',
            mode: 'lines+points',
            marker: {
              size: 5,
              color: 'blue',
              colorscale: 'Viridis',
              opacity: 0.8,
            },
          },
        ]}
      />
    </div>
  );
}

export default PlotlyComponent;
