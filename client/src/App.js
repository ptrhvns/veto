import NotFound from './pages/NotFound';
import SignUp from './pages/SignUp';
import Welcome from './pages/Welcome';
import { HelmetProvider } from 'react-helmet-async';
import { Route, Switch } from 'react-router-dom';

function App() {
  return (
    <>
      <HelmetProvider>
        <Switch>
          <Route exact path="/">
            <Welcome />
          </Route>
          <Route path="/sign-up">
            <SignUp />
          </Route>
          <Route path="*">
            <NotFound />
          </Route>
        </Switch>
      </HelmetProvider>
    </>
  );
}

export default App;
