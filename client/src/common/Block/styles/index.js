import styled from 'styled-components';

export const Block = styled.section`
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 7.5rem 0 0;

  @media screen and (max-width: 768px) {
    padding: 5.5rem 0 3rem;
  }
`;

export const Content = styled.p`
  padding: 4rem 0 0;
  font-size: 1.5rem;
`;

export const ContentWrapper = styled.div`
  max-width: 570px;
  @media only screen and (max-width: 768px) {
    max-width: 100%;
  }
`;

export const Logo = styled.img`
  width: 300px;
  height: 300px;
`;
