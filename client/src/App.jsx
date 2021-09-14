import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';

import './App.css';
import { ThemeProvider } from 'styled-components';

import callAPI from './api';
import Block from './common/Block';
import Container from './common/Container';
import Header from './components/Header';
import PlotlyComponent from './components/Plotly';
import { BrowserRouter as Router } from 'react-router-dom';
import { GlobalStyles } from './common/GlobalStyle';

import { settheme } from './common/ThemeSlice';
import { lightTheme, darkTheme } from './common/ThemeStyle';

function App() {
  const useDarkMode = () => {
    const [theme, setTheme] = useState('');

    const today = new Date();
    const hour = today.getHours();

    useEffect(() => {
      if (hour > 18) {
        setTheme('night');
      } else {
        setTheme('day');
      }
    }, [hour]);

    return [theme];
  };

  const dispatch = useDispatch();
  const [theme, themeToggler] = useDarkMode();

  dispatch(settheme(theme));
  const themeMode = theme === 'day' ? lightTheme : darkTheme;

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
    return (
      <ThemeProvider theme={themeMode}>
        <GlobalStyles />

        <h1
          style={{
            color: themeMode.text,
          }}
        >
          Loading
        </h1>
      </ThemeProvider>
    );
  }
}

export default App;
