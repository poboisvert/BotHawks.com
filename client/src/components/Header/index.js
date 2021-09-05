import React, { Component } from 'react';
import * as S from './styles';
import { Link } from 'react-scroll';

export default function Header() {
  return (
    <>
      <S.Container id='home'>
        <S.CustomNavLinkSmall>
          <S.Span>
            <Link to='chart' spy={true} smooth={true}>
              Chart
            </Link>
          </S.Span>
        </S.CustomNavLinkSmall>
        <S.CustomNavLinkSmall>
          <S.Span>
            <Link to='mission' spy={true} smooth={true}>
              Mission
            </Link>
          </S.Span>
        </S.CustomNavLinkSmall>
        <S.CustomNavLinkSmall>
          <S.Span>
            <Link to='home' spy={true} smooth={true}>
              First!
            </Link>
          </S.Span>
        </S.CustomNavLinkSmall>
      </S.Container>
    </>
  );
}
