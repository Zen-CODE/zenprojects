import React, { Component } from 'react';
// import WelcomePageContent from './welcome.component';
import { withWebId } from '@inrupt/solid-react-components';
import data from '@solid/query-ldflex';
import { withToastManager } from 'react-toast-notifications';

const defaultProfilePhoto = '/img/icon/empty-profile.svg';

/**
 * Container component for the Welcome Page, containing example of how to fetch data from a POD
 */
class TunezComponent extends Component<Props> {
  constructor(props) {
    super(props);

    // this.state = {
    //   name: '',
    //   image: defaultProfilePhoto,
    //   isLoading: false,
    //   hasImage: false
    // };
  }
  componentDidMount() {
    if (this.props.webId) {
      this.getProfileData();
    }
  }

  render() {
    return (
        <p>This be the Tunez Component</p>
    )
  }
}

export default withWebId(withToastManager(TunezComponent));
