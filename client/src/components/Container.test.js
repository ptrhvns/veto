import Container from './Container';
import React from 'react';
import ReactDOM from 'react-dom';

it('renders successfully', () => {
  const div = document.createElement('div');
  ReactDOM.render(
    <Container variant="viewport">
      <div>Test content.</div>
    </Container>,
    div
  );
});
