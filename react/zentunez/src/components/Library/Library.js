import React from 'react';
import './Library.css';

export class Library extends Component {
    /**
     * This component displays the volume slider
     */    
    constructor(props) {
        super(props);
      };

    render(){
      return (
        <div className="LibraryPanel">
          <p><b>ZenTunez Library</b></p>
        </div>
      );
    }
  }