import React from 'react';
import card1 from '.././images/card1.jpg';
import card2 from '.././images/card2.jpg';
import card3 from '.././images/card3.jpg';

export default function Cards() {
  return (
    <div className="d-flex mt-5 justify-content-center">
      <div className="mx-5 mb-3">
        <img className="card-img-top" src={card1} alt="Card image cap"/>
        <div className="card-body col text-center">
          <h2 className="card-title">Get started with Innotter</h2>
          <p className="card-text text-wrap card-credentials">New to Innotter? Explore these resources to know what to expect along the way.</p>
          <a className="btn btn-primary" href="https://github.com/amarjin6/">View details »</a>
        </div>
      </div>
      <div className="mx-5 mb-3">
        <img className="card-img-top" src={card2} alt="Card image cap"/>
        <div className="card-body col text-center">
          <h2 className="card-title">2022 Global Messenger Survey</h2>
          <p className="card-text text-wrap card-credentials">See what we learned from over 1,000 professionals about speed, security and performance.</p>
          <a className="btn btn-primary" href="https://github.com/amarjin6/">View details »</a>
        </div>
      </div>
      <div className="mx-5 mb-3">
        <img className="card-img-top" src={card3} alt="Card image cap"/>
        <div className="card-body col text-center">
          <h2 className="card-title">See what you could do</h2>
          <p className="card-text text-wrap card-credentials">Communicate and stay connected through the exchange of quick, frequent messages.</p>
          <a className="btn btn-primary" href="https://github.com/amarjin6/">View details »</a>
        </div>
      </div>
    </div>
    
  );
}
