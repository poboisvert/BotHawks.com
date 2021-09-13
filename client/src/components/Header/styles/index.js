import styled from 'styled-components';

export const Container = styled.div`
  position: sticky;
  top: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-color: #f0f6f0;

  padding-top: 10px;
  z-index: 999;

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
  text-align: center;

  @media only screen and (max-width: 768px) {
    margin: 1.25rem 2rem;
  }
`;

export const Span = styled.span`
  align-items: center;
  justify-content: center;
  text-align: center;
  cursor: pointer;
`;
