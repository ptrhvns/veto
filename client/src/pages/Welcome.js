import Container from '../components/Container';
import { buildTitle } from '../lib/utils';
import {
  faArrowAltCircleDown,
  faChevronRight,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { Helmet } from 'react-helmet-async';
import { Link } from 'react-router-dom';

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
              <Link className="welcome-hero-link" to="/sign-up">
                Sign up
                <FontAwesomeIcon
                  className="welcome-hero-link-icon"
                  icon={faChevronRight}
                />
              </Link>
            </div>
          </Container>
        </Container>
      </div>
    </>
  );
}

export default Welcome;
