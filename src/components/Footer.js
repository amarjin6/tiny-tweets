import React from 'react';
import { MDBFooter, MDBContainer, MDBRow, MDBCol, MDBIcon } from 'mdb-react-ui-kit';
import * as Icon from 'react-bootstrap-icons';

export default function Footer() {
  return (
    <MDBFooter bgColor='grey' className='text-center text-lg-start text-muted' style={{ backgroundColor: 'rgba(0, 0, 0, 0.09)' }}>
      <section className='d-flex justify-content-center justify-content-lg-between p-4 border-bottom'>
        <div className='me-5 d-none d-lg-block'>
          <span>Get connected with us on social networks:</span>
        </div>
        <div className='d-flex justify-content-center'>
          <a href='https://github.com/amarjin6/' className='me-4 text-reset'>
            <Icon.Facebook/>
          </a>
          <a href='https://github.com/amarjin6/' className='me-4 text-reset'>
            <Icon.Telegram/>
          </a>
          <a href='https://github.com/amarjin6/' className='me-4 text-reset'>
            <Icon.Google/>
          </a>
          <a href='https://github.com/amarjin6/' className='me-4 text-reset'>
            <Icon.Instagram/>
          </a>
          <a href='https://github.com/amarjin6/' className='me-4 text-reset'>
            <Icon.Linkedin/>
          </a>
          <a href='https://github.com/amarjin6/' className='me-4 text-reset'>
            <Icon.Github/>
          </a>
        </div>
      </section>

      <section className=''>
        <MDBContainer className='text-center text-md-start mt-5'>
          <MDBRow className='mt-3'>
            <MDBCol md='3' lg='4' xl='3' className='mx-auto mb-4'>
              <h6 className='text-uppercase fw-bold mb-4'>
                <MDBIcon color='secondary' icon='gem' className='me-3' />
                    Innotter
              </h6>
              <p>
                Innotter - is a microblogging, social networking service, on which users post and interact with
                messages known as "tweets".
              </p>
            </MDBCol>

            <MDBCol md='2' lg='2' xl='2' className='mx-auto mb-4'>
              <h6 className='text-uppercase fw-bold mb-4'>Resources</h6>
              <p>
                <a href='#docs' className='text-reset'>
                  Docs
                </a>
              </p>
              <p>
                <a href='#blog' className='text-reset'>
                  Blog
                </a>
              </p>
              <p>
                <a href='#community' className='text-reset'>
                  Community
                </a>
              </p>
              <p>
                <a href='#learn' className='text-reset'>
                  Learn
                </a>
              </p>
            </MDBCol>

            <MDBCol md='3' lg='2' xl='2' className='mx-auto mb-4'>
              <h6 className='text-uppercase fw-bold mb-4'>Company</h6>
              <p>
                <a href='#about' className='text-reset'>
                    About
                </a>
              </p>
              <p>
                <a href='#jobs' className='text-reset'>
                    Jobs
                </a>
              </p>
              <p>
                <a href='#events' className='text-reset'>
                    Events
                </a>
              </p>
              <p>
                <a href='#help' className='text-reset'>
                    Help
                </a>
              </p>
            </MDBCol>

            <MDBCol md='4' lg='3' xl='3' className='mx-auto mb-md-0 mb-4'>
              <h6 className='text-uppercase fw-bold mb-4'>Contact us</h6>
              <p>
                <MDBIcon color='secondary' icon='home' className='me-1' />
                    Minsk, Belarus 
              </p>
              <p>
                <a href="mailto:innotter@gmail.com" className='footer-credentials'>
                    <Icon.Mailbox className='me-1'/>
                    innotter@gmail.com
                </a>
              </p>
              <p>
                <a href="tel:3751234567" className='footer-credentials'>
                    <Icon.Telephone className='me-1'/>
                    +375-123-45-67
                </a>
              </p>
              <p>
                <a href="tel:3758910112" className='footer-credentials'>
                    <Icon.TelephoneFill className='me-1'/>
                    +375-891-01-12
                </a>
              </p>
            </MDBCol>
          </MDBRow>
        </MDBContainer>
      </section>

      <div className='text-center p-4' style={{ backgroundColor: 'rgba(0, 0, 0, 0.09)' }}>
        © 2022 Copyright:
        <a className='text-reset fw-bold' href='https://github.com/amarjin6/'>
          Innotter.com
        </a>
      </div>
    </MDBFooter>
  );
}
