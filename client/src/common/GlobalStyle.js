import { createGlobalStyle } from 'styled-components';

export const GlobalStyles = createGlobalStyle`
  body {
    background: ${({ theme }) => theme.background};
    color: ${({ theme }) => theme.text};
  }
  a {
    text-decoration: none;
    outline: none;
    color: ${({ theme }) => theme.link};
    :hover {
      color: ${({ theme }) => theme.link};
    }
  }
  
  `;
