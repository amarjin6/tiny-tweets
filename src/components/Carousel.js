import React from 'react';
import "bootstrap/dist/css/bootstrap.min.css"
import carousel1 from '.././images/carousel1.jpg';
import carousel2 from '.././images/carousel2.jpg';
import carousel3 from '.././images/carousel3.jpg';
import Carousel from 'react-bootstrap/Carousel';

export default function ControlledCarousel() {
  return (
    <Carousel>
        <Carousel.Item interval={1000}>
        <img
            className="d-block w-100"
            src={carousel1}
            alt="First slide"
        />
        <Carousel.Caption>
            <h3>Stay up to date</h3>
            <p>Get a daily news briefing and market updates in Messenger.</p>
        </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item interval={1000}>
        <img
            className="d-block w-100"
            src={carousel2}
            alt="Second slide"
        />
        <Carousel.Caption>
            <h3>Entertainment area</h3>
            <p>Browse shows, videos, and other entertainment with us.</p>
        </Carousel.Caption>
        </Carousel.Item>
        <Carousel.Item interval={1000}>
        <img
            className="d-block w-100"
            src={carousel3}
            alt="Third slide"
        />
        <Carousel.Caption>
            <h3>Keep in touch</h3>
            <p>Register now and get in touch with great people.</p>
        </Carousel.Caption>
        </Carousel.Item>
    </Carousel>
    );
  }