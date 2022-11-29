import React from "react";
import logo from '.././images/logo.png';
import * as Icon from 'react-bootstrap-icons';

const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <a className="navbar-brand" href="#home">
            <img
              alt="Innotter logo"
              src={logo}
              width="30"
              height="30"
              className="d-inline-block align-top navbar-logo"
            />
            Innotter
            </a>
            <button className="navbar-toggler" type="button" data-toggler="collapse"
            data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
            aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>

            <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav mr-auto">
                    <li className="nav-item active">
                        <a className="nav-link" href="#home"><span className="sr-only"><Icon.House/></span>Home</a>
                    </li>
                    <li className="nav-item active">
                        <a className="nav-link" href="#feed"><span className="sr-only"><Icon.PersonBoundingBox/></span>Feed</a>
                    </li>
                    <li className="nav-item active">
                        <a className="nav-link" href="#posts"><span className="sr-only"><Icon.EnvelopePaper/></span>Posts</a>
                    </li>
                    <li className="nav-item active">
                        <a className="nav-link" href="#pages"><span className="sr-only"><Icon.JournalBookmarkFill/></span>Pages</a>
                    </li>
                </ul>
            </div>
            <form className="form-inline">
                <div className="navbar-form">
                    <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
                    <button className="btn btn-outline-primary my-2 my-sm-0 navbar-form-button" type="submit">Search</button>
                </div>
            </form>
            <div className="navbar-label">Signed in as: <a href="#login" className="navbar-label-link">Anonymous User</a></div>
        </nav>
    )
}

export default Navbar