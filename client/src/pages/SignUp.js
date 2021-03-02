import { buildTitle } from '../lib/utils';
import { Helmet } from 'react-helmet-async';

function SignUp() {
  return (
    <>
      <Helmet>
        <title>{buildTitle('Sign Up')}</title>
      </Helmet>

      <div data-testid="sign-up">Sign Up</div>
    </>
  );
}

export default SignUp;
