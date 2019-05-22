import React, { Component } from 'react';
import { withWebId } from '@inrupt/solid-react-components';
import data from '@solid/query-ldflex';
import { withToastManager } from 'react-toast-notifications';

/**
 * Container component for the Tunez Page
 */
class TunezComponent extends Component<Props> {
  constructor(props) {
    super(props);

    this.state = {
      name: '',
      isLoading: false
    };
  }
  componentDidMount() {
    if (this.props.webId) {
      this.getProfileData();
    }
  }

  componentDidUpdate(prevProps, prevState) {
    if (this.props.webId && this.props.webId !== prevProps.webId) {
      this.getProfileData();
    }
  }  

  getProfileData = async () => {
    this.setState({ isLoading: true });

    /*
     * This is an example of how to use LDFlex. Here, we're loading the webID link into a user variable. This user object
     * will contain all of the data stored in the webID link, such as profile information. Then, we're grabbing the user.name property
     * from the returned user object.
     */
    const user = data[this.props.webId];
    const nameLd = await user.name;
    const name = nameLd ? nameLd.value : '';

    this.setState({ name: name, isLoading: false });
  };

  render() {
    return (
        <p>This be the Tunez Component for { this.state.name }! </p>
    )
  }
}

export default withWebId(withToastManager(TunezComponent));
