import styled from 'styled-components';

export const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 1280px;

  position: fixed;
  top: 0;
  z-index: 10;
  background-color: #fff;
  margin: 20px 0 0 20px;

  @media only screen and (max-width: 768px) {
    width: 340px;
    justify-content: center;
    align-items: center;
  }
`;

export const CustomNavLinkSmall = styled.div`
  font-size: 1rem;
  color: black;
  transition: color 0.2s ease-in;
  margin: 0.25rem 2rem;

  @media only screen and (max-width: 768px) {
    margin: 1.25rem 2rem;
  }
`;

export const Span = styled.span`
  align-items: center;
  justify-content: center;
  cursor: pointer;
`;
