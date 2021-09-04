import React, { useState, useEffect } from 'react';
import callAPI from './api';
import PlotlyComponent from './Plotly';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [latestPrice, setLatestPrice] = useState(0);
  const [data, setData] = useState(0);

  const fetchData = async () => {
    let data = { index: [], price: [], volumes: [] };
    let result = await callAPI(
      'https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=1&interval=1m'
    );
    for (const item of result.prices) {
      data.index.push(item[0]);
      data.price.push(item[1]);
    }
    for (const item of result.total_volumes) data.volumes.push(item[1]);
    return data;
  };

  useEffect(() => {
    fetchData().then((chartData) => {
      setIsLoading(false);
      setData(chartData);
      setLatestPrice(
        parseFloat(chartData.price[chartData.price.length - 1]).toFixed(2)
      );
    });
    const timerID = setInterval(() => {
      fetchData().then((chartData) => {
        setLatestPrice(
          parseFloat(chartData.price[chartData.price.length - 1]).toFixed(2)
        );
        setData(chartData);
      });
    }, 1000 * 10);
    return () => {
      clearInterval(timerID);
    };
  }, []);
  console.log(latestPrice);

  return (
    <div className='App'>
      <header className='App-header'>
        <p>
          <PlotlyComponent data={data} />
        </p>
      </header>
    </div>
  );
}

export default App;
