import NotFound from './NotFound';
import Welcome from './Welcome';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { buildTitle } from '../lib/utils';
import { Helmet, HelmetProvider } from 'react-helmet-async';

function App() {
  return (
    <>
      <HelmetProvider>
        <Helmet>
          <title>{buildTitle()}</title>
        </Helmet>

        <Router>
          <Switch>
            <Route exact path="/">
              <Welcome />
            </Route>
            <Route path="*">
              <NotFound />
            </Route>
          </Switch>
        </Router>
      </HelmetProvider>
    </>
  );
}

export default App;
