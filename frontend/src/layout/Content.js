import React, {useEffect, useState} from "react";
import Divider from "../components/Divider";
import FeedList from "../components/FeedList";
import TweetBox from "../components/TweetBox";
import {PopulerIcon} from "../icons/Icon";
import TweetService from "../service/TweetService";
import profile from "../images/default-profile.png";
import {useSelector} from "react-redux";

const Content = () => {
    const [tweets, setTweets] = useState([]);
    const [render, setRender] = useState(false)

    const profileImageLink = useSelector(state => state.reduxSlice.profileImageLink)

    const accessToken = useSelector(state => state.reduxSlice.accessToken)

     let config = {
        headers: {
            'Authorization': 'Bearer ' + accessToken
        }
     }

    useEffect(() => {
        let tweetService = new TweetService()
        tweetService.getTweets(config).then(res => setTweets(res.data))
    }, [render]);

    const refreshTweets = () => {
        setRender(!render)
    }

    return (
        <main className="flex flex-col border-r border-l border-gray-extraLight w-1/2 mr-auto">
            <header
                className="sticky top-0 z-10 bg-white flex justify-between items-center p-4 h-16 border-b border-gray-extraLight ">
                <span className="font-bold text-xl text-gray-900">Home</span>
                <PopulerIcon className="w-6 h-6 text-primary-base"/>
            </header>
            <div className="flex space-x-4 px-4 py-3">
                <img
                    src={profileImageLink ? profileImageLink : profile}
                    alt="Profile"
                    className="w-11 h-11 rounded-full"
                />
                <TweetBox refresh={refreshTweets}/>
            </div>
            <Divider/>
            <FeedList tweets={tweets}/>
        </main>
    );
};

export default Content;
