import React, { Component } from 'react';
import { withWebId } from '@inrupt/solid-react-components';
// import data from '@solid/query-ldflex';
import { withToastManager } from 'react-toast-notifications';

/**
 * Container component for the Tunez Page
 */
class TunezComponent extends Component<Props> {
  constructor(props) {
    super(props);

    this.state = {
      name: ''
    };
  }
  componentDidMount() {
    if (this.props.webId) {
      this.getProfileData();
    }
  }

  render() {
    return (
        <p>This be the Tunez Component for { this.state.name }! </p>
    )
  }
}

export default withWebId(withToastManager(TunezComponent));
