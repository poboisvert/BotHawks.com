import React from 'react';
import * as S from './styles';
import { Link } from 'react-scroll';
import { useSelector } from 'react-redux';
import { selectTheme } from '../../common/ThemeSlice';
import { lightTheme, darkTheme } from '../../common/ThemeStyle';

export default function Header() {
  const theme = useSelector(selectTheme);

  const themeMode = theme === 'day' ? lightTheme : darkTheme;

  return (
    <>
      <S.Container
        id='home'
        style={{
          textDecoration: 'none',
          backgroundColor: themeMode.background,
        }}
      >
        <S.CustomNavLinkSmall>
          <S.Span>
            <Link
              style={{
                textDecoration: 'none',
                color: themeMode.text,
              }}
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
              style={{
                textDecoration: 'none',
                color: themeMode.text,
              }}
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
              style={{ textDecoration: 'none', color: themeMode.text }}
              to='home'
              spy={true}
              smooth={true}
            >
              First
            </Link>
          </S.Span>
        </S.CustomNavLinkSmall>
      </S.Container>
    </>
  );
}
