import * as S from './styles';
import logo from '../logo.png';
import logo_night from '../logo_night.png';

import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';

import { useSelector } from 'react-redux';
import { selectTheme } from '../ThemeSlice';
import { lightTheme, darkTheme } from '../ThemeStyle';

// BrowserRouter is the router implementation for HTML5 browsers (vs Native).
// Link is your replacement for anchor tags.
// Route is the conditionally shown component based on matching a path to a URL.
// Switch returns only the first matching route rather than all matching routes.

const Block = (props) => {
  const logoMode = props.logo === 'logo' ? logo : logo_night;
  const theme = useSelector(selectTheme);

  const themeMode = theme === 'day' ? lightTheme : darkTheme;

  return (
    <S.Block id='mission'>
      <S.ContentWrapper>
        <S.Logo src={logoMode} />
        <S.Content
          style={{
            color: themeMode.text,
          }}
        >
          {props.content} <br />
          <Link
            to={{ pathname: 'https://github.com/poboisvert/BotHawks.com' }}
            target='_blank'
          >
            GitHub Project
          </Link>
        </S.Content>
      </S.ContentWrapper>
    </S.Block>
  );
};

export default Block;
