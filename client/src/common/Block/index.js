import * as S from './styles';
import logo from '../logo.png';
import logo_nigh from '../logo_night.png';

import { Link } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
// BrowserRouter is the router implementation for HTML5 browsers (vs Native).
// Link is your replacement for anchor tags.
// Route is the conditionally shown component based on matching a path to a URL.
// Switch returns only the first matching route rather than all matching routes.

const Block = ({ content }) => {
  const [logo, setLogo] = useState('');
  const [today, setDate] = useState(new Date()); // Save the current date to be able to trigger an update

  useEffect(() => {
    let result = 0;
    const logos = [logo, logo_nigh];

    const hour = today.getHours();
    if (hour > 17) {
      setLogo(logos[1]);
    } else {
      setLogo(logos[0]);
    }
  }, [content]);
  return (
    <S.Block id='mission'>
      <S.ContentWrapper>
        <S.Logo src={logo} />
        <S.Content>
          {content} <br />
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
