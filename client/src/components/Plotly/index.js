import React from 'react';
import Plot from 'react-plotly.js';
import * as S from './styles';

function Plotly({ data, background, text }) {
  return (
    <S.ContentWrapper id='chart'>
      <Plot
        useResizeHandler
        style={{ width: '100%' }}
        layout={{
          // width: 320,
          // height: 240,
          autosize: true,
          dragmode: true,
          plot_bgcolor: background,
          paper_bgcolor: background,
          margin: {
            l: 0,
            r: 0,
            t: 10,
            b: 10,
            pad: 10,
            autoexpand: true,
          },
        }}
        data={[
          {
            // setIsPreview(data.index.map((t) => new Date(t)))
            x: data.index.map((t) => new Date(t)),
            y: data.price,
            z: data.volume,
            type: 'scatter',
            mode: 'lines+points',
            marker: {
              size: 5,
              color: text,
              colorscale: 'Viridis',
              opacity: 0.8,
            },
          },
        ]}
      />
    </S.ContentWrapper>
  );
}

export default Plotly;
