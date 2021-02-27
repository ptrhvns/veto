import Container from '../components/Container';
import { buildTitle } from '../lib/utils';
import {
  faArrowAltCircleDown,
  faChevronRight,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Helmet } from 'react-helmet-async';

function Welcome() {
  return (
    <>
      <Helmet>
        <title>{buildTitle('Welcome')}</title>
      </Helmet>

      <div data-testid="welcome">
        <Container className="welcome-hero-viewport" variant="viewport">
          <Container className="welcome-hero-content" variant="content">
            <div>
              <h1 className="welcome-hero-title">
                VETO
                <FontAwesomeIcon
                  className="welcome-hero-title-icon"
                  icon={faArrowAltCircleDown}
                />
              </h1>
              <h2 className="welcome-hero-subtitle">Make decisions faster.</h2>
              <a className="welcome-hero-link">
                Get Started
                <FontAwesomeIcon
                  className="welcome-hero-link-icon"
                  icon={faChevronRight}
                />
              </a>
            </div>
          </Container>
        </Container>
      </div>
    </>
  );
}

export default Welcome;
