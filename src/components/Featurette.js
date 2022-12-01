import React from 'react';
import featurette1 from '.././images/featurette1.jpg';
import featurette2 from '.././images/featurette2.jpg';
import featurette3 from '.././images/featurette3.jpg';

export default function Featurette() {
    return (
        <>
        <hr className="featurette-divider" />
        <div className="d-flex justify-content-between">
            <div className="text-wrap featurette-text-left">
                <h2 className="featurette-heading text-wrap">Once you try, you will never stop.
                    <span className="text-muted">It’ll blow your mind.</span>
                </h2>
                <p className="text-wrap lead">Innotter can be used by millions of users that can be the best opportunity to reach future customers.</p>
            </div>
            <div className="featurette-object">
                <img className="media-object featurette-image-right" src={featurette1} alt="Featurette 1"/>
            </div>
        </div>
        <hr className="featurette-divider" />
        <div className="d-flex justify-content-between">
            <div className="featurette-object">
                <img className="media-object featurette-image-left" src={featurette2} alt="Featurette 1"/>
            </div>
            <div className="text-wrap featurette-text-right">
                <h2 className="featurette-heading text-wrap">Oh yeah, it’s that good.
                    <span className="text-muted">See for a recent connections.</span>
                </h2>
                <p className="text-wrap lead">Direct interaction with others is easier through hashtags we can directly approach the targeted audience.</p>
            </div>
        </div>
        <hr className="featurette-divider" />
        <div className="d-flex justify-content-between">
            <div className="text-wrap featurette-text-left">
                <h2 className="featurette-heading text-wrap">And lastly, this one.
                    <span className="text-muted">Checkmate.</span>
                </h2>
                <p className="text-wrap lead">The interested audience for a particular topic can be reached out very quickly fo free.</p>
            </div>
            <div className="featurette-object">
                <img className="media-object featurette-image-right" src={featurette3} alt="Featurette 1"/>
            </div>
        </div>
        <hr className="featurette-divider" />
        </>
    )
}
