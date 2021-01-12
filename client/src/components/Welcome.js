import { buildTitle } from '../lib/utils';
import { Helmet } from 'react-helmet-async';

function Welcome() {
  return (
    <>
      <Helmet>
        <title>{buildTitle('Welcome')}</title>
      </Helmet>

      <div>Welcome</div>
    </>
  );
}

export default Welcome;
