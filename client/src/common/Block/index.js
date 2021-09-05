import * as S from './styles';
import Logo from '../logo.png';

const Block = ({ content }) => {
  return (
    <S.Block id='mission'>
      <S.ContentWrapper>
        <S.Logo src={Logo} />
        <S.Content>{content}</S.Content>
      </S.ContentWrapper>
    </S.Block>
  );
};

export default Block;
