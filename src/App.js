import './App.css';
import "bootstrap/dist/css/bootstrap.min.css"
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ControlledCarousel from './components/Carousel';
import Cards from './components/Cards'

function App() {
  return (
    <>
      <Navbar />
      <ControlledCarousel />
      <Cards />
      <Footer />
    </>
  );
}

export default App;
