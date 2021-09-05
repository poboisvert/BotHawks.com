import React, { useState } from 'react';
import Plot from 'react-plotly.js';
import * as S from './styles';

function Plotly({ data }) {
  return (
    <S.ContentWrapper>
      <Plot
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
              color: 'blue',
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
