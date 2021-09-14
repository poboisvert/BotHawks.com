import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { useDispatch } from 'react-redux';

import { ThemeProvider } from 'styled-components';
import { useDarkMode } from './common/ThemeAction';

import callAPI from './api';
import Block from './common/Block';
import Container from './common/Container';
import Header from './components/Header';
import PlotlyComponent from './components/Plotly';
import { BrowserRouter as Router } from 'react-router-dom';
import './App.css';
import { selectTheme } from './common/ThemeSlice';
import { GlobalStyles } from './common/GlobalStyle';

import { settheme } from './common/ThemeSlice';
import { lightTheme, darkTheme } from './common/ThemeStyle';

function App() {
  const [theme, themeToggler] = useDarkMode();
  const dispatch = useDispatch();

  dispatch(settheme(theme));

  const theme_original = useSelector(selectTheme);

  const themeMode = theme === 'day' ? lightTheme : darkTheme;

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
    }, 1000 * 2);
    return () => {
      clearInterval(timerID);
    };
  }, []);

  console.log(latestPrice);

  if (data) {
    return (
      <>
        <Router>
          <ThemeProvider theme={themeMode}>
            <>
              <GlobalStyles />
              <Header />
              <Container>
                <Block
                  logo={themeMode.logo}
                  content='Our mission is to offer Coinbase live data'
                />
                <PlotlyComponent
                  data={data}
                  background={themeMode.background}
                  text={themeMode.text}
                />
              </Container>
            </>
          </ThemeProvider>
        </Router>
      </>
    );
  } else {
    return <h1>Loading</h1>;
  }
}

export default App;
