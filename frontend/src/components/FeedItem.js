import React, {useEffect, useState} from "react";
import {ReplyIcon, ReTweetIcon, ShareIcon} from "../icons/Icon";
import profile from '../images/default-profile.png'
import FavoriteIcon from '@mui/icons-material/Favorite';
import FavoriteBorderIcon from '@mui/icons-material/FavoriteBorder';
import LikeService from "../service/LikeService";
import Modal from "./Modal";
import {useNavigate} from "react-router-dom";
import {useSelector} from "react-redux";
import UserService from "../service/UserService";

const FeedItem = ({
    uuid,
    title,
    tags,
    image,
    description,
    owner,
    followers,
    is_private,
    is_blocked,
    created_at
}) => {
    const userService = new UserService()
    const [user, setUser] = useState()
    const accessToken = useSelector(state => state.reduxSlice.accessToken)

    let config = {
        headers: {
            'Authorization': 'Bearer ' + accessToken
        }
     }

    useEffect(() => {
        userService.getUserByUsername(config, owner.id)
            .then(res => setUser(res.data))
            .catch(error => console.error("Error fetching user data:", error));
    }, [owner.id]);

    const navigate = useNavigate()
    return (
    <>
        {user && (
            <article className="flex space-x-3 border-b border-gray-extraLight px-4 py-3 cursor-pointer">
            <img src={user.image ? user.image : profile} alt="Profile" className="w-11 h-11 rounded-full" onClick={() => navigate("/" + owner.id)} />
            <div className="flex-1">
                <div className="flex items-center text-sm">
                    <h4 className="font-bold">{title}</h4>
                    <span className="ml-2 text-gray-dark">@{owner.username}</span>
                    <div className="mx-2 bg-gray-dark h-1 w-1 border rounded-full" />
                    <span className="text-gray-dark">
                        {created_at ? new Date(created_at).toLocaleString("tr-TR") : ""}
                    </span>
                </div>
                <span className="bg-green-100 text-green-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2">
                    {uuid}
                </span>
                <div className="flex flex-wrap items-center mt-3">
                    {tags.map((tag) => (
                        <span key={tag.id} className="bg-blue-100 text-blue-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2">
                            {tag.name}
                        </span>
                    ))}
                </div>
                <span className={`bg-red-100 text-red-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2 ${is_private ? 'true' : 'hidden'}`}>
                    Private
                </span>
                <span className={`bg-red-100 text-red-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2 ${is_blocked ? 'true' : 'hidden'}`}>
                    Blocked
                </span>
                <p className="mt-2 text-gray-900 text-sm">{description}</p>
                {image && <img src={image} className="my-2 rounded-xl max-h-96" alt={title} />}
                <ul className="-ml-1 mt-3 flex justify-between max-w-md">
                    {followers.map((follower) => (
                        <li key={follower.id} className="flex items-center text-gray-dark text-sm group">
                            <span className="bg-pink-100 text-pink-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2">@{follower.username}</span>
                        </li>
                    ))}
                </ul>
            </div>
        </article>
        )}
    </>
    )
};

export default FeedItem;
