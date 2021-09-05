import * as S from './styles';
import Logo from '../logo.png';
import { Link } from 'react-router-dom';
// BrowserRouter is the router implementation for HTML5 browsers (vs Native).
// Link is your replacement for anchor tags.
// Route is the conditionally shown component based on matching a path to a URL.
// Switch returns only the first matching route rather than all matching routes.

const Block = ({ content }) => {
  return (
    <S.Block id='mission'>
      <S.ContentWrapper>
        <S.Logo src={Logo} />
        <S.Content>
          {content} <br />
          <Link
            to={{ pathname: 'https://github.com/poboisvert/BotHawks.com' }}
            target='_blank'
          >
            GitHub Project
          </Link>
        </S.Content>
      </S.ContentWrapper>
    </S.Block>
  );
};

export default Block;
