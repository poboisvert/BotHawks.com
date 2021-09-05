import styled from 'styled-components';

export const ContentWrapper = styled.div`
  display: flex;
  text-align: center;
  justify-content: center;

  @media screen and (max-width: 768px) {
    padding: 5.5rem 0 3rem;
    max-width: 320px;
  }
`;
