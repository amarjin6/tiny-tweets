import React from "react";
import {useSelector} from "react-redux";
import Home from "./pages/Home";
import {Route, Routes} from "react-router-dom";
import Login from "./layout/Login";
import Signup from "./layout/Signup";
import Tweet from "./pages/Tweet";
import Statistic from "./pages/Statistic";
import Container from "./layout/Container";
import Sidebar from "./layout/Sidebar";
import Content from "./layout/Content";
import Widgets from "./layout/Widgets";
import User from "./pages/User";

const App = () => {
    const currentUser = useSelector(state => state.reduxSlice.currentUser)
    return (
        <>
            {currentUser ?
                <Container>
                    <Sidebar/>
                    <Routes>
                        <Route path='/' element={<Content/>}/>
                        <Route path="/pages/:id" element={<Tweet/>}/>
                        <Route path=":username" element={<User/>}/>
                        <Route path="/statistic" element={<Statistic/>}/>
                    </Routes>
                    <Widgets/>
                </Container> :
                <Routes>
                    <Route path='*' element={<Home/>}/>
                    <Route path='/login' element={<Login/>}/>
                    <Route path='/signup' element={<Signup/>}/>
                </Routes>
            }
        </>
    );
};

export default App;
