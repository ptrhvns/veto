import { buildTitle } from '../lib/utils';
import { Helmet } from 'react-helmet-async';

function Welcome() {
  return (
    <>
      <Helmet>
        <title>{buildTitle('Welcome')}</title>
      </Helmet>

      <div data-testid="welcome">
        <div>Welcome</div>
      </div>
    </>
  );
}

export default Welcome;
