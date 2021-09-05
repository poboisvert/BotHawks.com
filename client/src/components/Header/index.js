import React from 'react';
import * as S from './styles';
// import { Container, Leftside, Rightside } from "./styles/Header";

export default function Header() {
  return (
    <>
      <S.Container>
        <S.CustomNavLinkSmall>
          <S.Span>Chart</S.Span>
        </S.CustomNavLinkSmall>
        <S.CustomNavLinkSmall>
          <S.Span>Mission</S.Span>
        </S.CustomNavLinkSmall>
        <S.CustomNavLinkSmall style={{ width: '180px' }}>
          <S.Span>
            <b>Introduction</b>
          </S.Span>
        </S.CustomNavLinkSmall>
      </S.Container>
    </>
  );
}
