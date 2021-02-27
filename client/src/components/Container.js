import _ from 'lodash';
import PropTypes from 'prop-types';
import React from 'react';

const propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  variant: PropTypes.oneOf(['content', 'viewport']).isRequired,
};

const defaultProps = {
  className: '',
};

function Container({ className, children, variant }) {
  const _className = _.join([`container-${variant}`, className], ' ');
  return <div className={_className}>{children}</div>;
}

Container.defaultProps = defaultProps;
Container.propTypes = propTypes;

export default Container;
