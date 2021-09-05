import React, { Component } from 'react';
import * as S from './styles';
import { Link } from 'react-scroll';

export default function Header() {
  return (
    <>
      <S.Container id='home'>
        <S.CustomNavLinkSmall>
          <S.Span>
            <Link
              style={{ textDecoration: 'none', color: '#222323' }}
              to='chart'
              spy={true}
              smooth={true}
            >
              Chart
            </Link>
          </S.Span>
        </S.CustomNavLinkSmall>
        <S.CustomNavLinkSmall>
          <S.Span>
            <Link
              style={{ textDecoration: 'none', color: '#222323' }}
              to='mission'
              spy={true}
              smooth={true}
            >
              Mission
            </Link>
          </S.Span>
        </S.CustomNavLinkSmall>
        <S.CustomNavLinkSmall>
          <S.Span>
            <Link
              style={{ textDecoration: 'none', color: '#222323' }}
              to='home'
              spy={true}
              smooth={true}
            >
              First!
            </Link>
          </S.Span>
        </S.CustomNavLinkSmall>
      </S.Container>
    </>
  );
}
