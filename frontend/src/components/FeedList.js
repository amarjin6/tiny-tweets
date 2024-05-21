import React, {useEffect, useState} from "react";
import FeedItem from "./FeedItem";
import {useSelector} from "react-redux";

const FeedList = ({tweets}) => {
    return (
       <div>
        {tweets
            .slice()
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            .map((tweet, index) => (
                <FeedItem
                    id={tweet.id}
                    uuid={tweet.uuid}
                    title={tweet.title}
                    tags={tweet.tags}
                    image={tweet.image}
                    description={tweet.description}
                    owner={tweet.owner}
                    followers={tweet.followers}
                    is_private={tweet.is_private}
                    is_blocked={tweet.is_blocked}
                    created_at={tweet.created_at}
                    key={index}
                />
            ))}
        </div>
    );
};

export default FeedList;
