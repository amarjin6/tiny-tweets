import React, { useEffect, useState, useCallback } from 'react';
import { useNavigate, useParams } from "react-router-dom";
import { ArrowBack } from "@mui/icons-material";
import { HeartFill, Heart } from 'react-bootstrap-icons';
import Divider from "../components/Divider";
import { useSelector } from "react-redux";
import profile from "../images/default-profile.png";
import TweetService from "../service/TweetService";
import axios from 'axios';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import Modal from '@mui/material/Modal';
import { Box, TextField, Button } from '@mui/material';

const Tweet = () => {
    const [tweet, setTweet] = useState(null);
    const [posts, setPosts] = useState([]);
    const [content, setContent] = useState('');
    const [replyTo, setReplyTo] = useState('');
    const [likedPosts, setLikedPosts] = useState([]);
    const [userImages, setUserImages] = useState({});
    const [openModal, setOpenModal] = useState(false);
    const [newTitle, setNewTitle] = useState('');
    const [newDescription, setNewDescription] = useState('');
    const { id } = useParams();
    const navigate = useNavigate();
    const accessToken = useSelector(state => state.reduxSlice.accessToken);
    const currentUser = useSelector(state => state.reduxSlice.currentUser);

    const config = {
        headers: {
            'Authorization': 'Bearer ' + accessToken
        }
    };

    const fetchUserImage = useCallback((userId) => {
        axios.get(`/api/v1/users/${userId}/`, config)
            .then(response => {
                setUserImages(prevImages => ({
                    ...prevImages,
                    [userId]: response.data.image
                }));
            })
            .catch(err => {
                console.error(err);
            });
    }, [config]);

    const refreshPosts = useCallback(() => {
        const tweetService = new TweetService();
        tweetService.getTweetsCommentByTweetId(id, config).then(res => {
            const sortedPosts = res.data
                .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            setPosts(sortedPosts);
            sortedPosts.forEach(post => fetchUserImage(post.owner.id));
        });
    }, [id, config, fetchUserImage]);

    useEffect(() => {
        const tweetService = new TweetService();
        tweetService.getTweetById(id, config).then(res => setTweet(res.data));
    }, [id]);

    useEffect(() => {
        refreshPosts();
    }, [id]);

    const handlePublish = () => {
        const post = {
            page: id,
            content,
        };

        if (replyTo) {
            post.reply_to = replyTo;
        }

        axios.post('/api/v1/posts/', post, config)
            .then(res => {
                setContent('');
                setReplyTo('');
                refreshPosts();
            })
            .catch(err => {
                console.error(err);
            });
    };

    const handleLike = (postId) => {
        const isLiked = likedPosts.includes(postId);

        axios.get(`/api/v1/posts/${postId}/like/`, config)
            .then(res => {
                if (isLiked) {
                    setLikedPosts(likedPosts.filter(id => id !== postId));
                } else {
                    setLikedPosts([...likedPosts, postId]);
                }
            })
            .catch(err => {
                console.error(err);
            });
    };

    const getPostContentById = (postId) => {
        const post = posts.find(post => post.id === postId);
        return post ? post.content : '';
    };

    const handleDelete = () => {
        axios.delete(`/api/v1/pages/${id}`, config)
            .then(() => {
                navigate('/');
            })
            .catch(err => {
                console.error(err);
            });
    };

    const handleOpenModal = () => {
        setNewTitle(tweet.title);
        setNewDescription(tweet.description);
        setOpenModal(true);
    };

    const handleCloseModal = () => {
        setOpenModal(false);
    };

    const handleSaveChanges = () => {
        const updatedTweet = {
            ...tweet,
            title: newTitle,
            description: newDescription,
            uuid: tweet.uuid,
            tags: tweet.tags,
            owner: tweet.owner,
            is_private: tweet.is_private
        };

        axios.patch(`/api/v1/pages/${id}/`, updatedTweet, config)
            .then(() => {
                setTweet(updatedTweet);
                setOpenModal(false);
            })
            .catch(err => {
                console.error(err);
            });
    };

    return (
        <>
            {tweet && (
                <div className="flex flex-col border-r border-l border-gray-extraLight w-1/2 mr-auto">
                    <header className="sticky top-0 z-10 bg-white flex justify-between items-center p-4 border-b border-gray-extraLight">
                        <span className="font-medium text-lg text-gray-900">
                            Posts from {tweet.title} page by @{tweet.owner.username}
                        </span>
                        <div className="flex items-center">
                            <ArrowBack className="w-6 h-6 text-primary-base cursor-pointer" onClick={() => navigate("/")} />
                        </div>
                    </header>
                    <Divider />
                    <article className="flex space-x-3 border-b border-gray-extraLight px-4 py-3 cursor-pointer">
                        <div className="flex-1">
                            <div className="flex items-center text-sm">
                                <h4 className="font-bold" onClick={() => navigate("/tweets/" + tweet.id)}>{tweet.title}</h4>
                                <span className="ml-2 text-gray-dark">@{tweet.owner.username}</span>
                                <div className="mx-2 bg-gray-dark h-1 w-1 border rounded-full" />
                                <span className="text-gray-dark">
                                    {tweet.created_at ? new Date(tweet.created_at).toLocaleString("tr-TR") : ""}
                                </span>
                                {parseInt(currentUser) === parseInt(tweet.owner.id) && (
                                <>
                                    <EditIcon className="w-6 h-6 text-gray-600 cursor-pointer ml-2" onClick={handleOpenModal} />
                                    <DeleteIcon className="w-6 h-6 text-red-600 cursor-pointer ml-2" onClick={handleDelete} />
                                </>
                            )}
                            </div>
                            <span className="bg-green-100 text-green-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2">
                                {tweet.uuid}
                            </span>
                            <div className="flex flex-wrap items-center mt-3">
                                {tweet.tags.map((tag) => (
                                    <span key={tag.id} className="bg-blue-100 text-blue-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2">
                                        {tag.name}
                                    </span>
                                ))}
                            </div>
                            <span className={`bg-red-100 text-red-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2 ${tweet.is_private ? 'true' : 'hidden'}`}>
                                Private
                            </span>
                            <span className={`bg-red-100 text-red-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2 ${tweet.is_blocked ? 'true' : 'hidden'}`}>
                                Blocked
                            </span>
                            <p className="mt-2 text-gray-900 text-sm">{tweet.description}</p>
                            {tweet.image && <img src={tweet.image ? tweet.image : profile} className="my-2 rounded-xl max-h-96" alt={tweet.title} />}
                            <ul className="-ml-1 mt-3 flex justify-between max-w-md">
                                {tweet.followers.map((follower) => (
                                    <li key={follower.id} className="flex items-center text-gray-dark text-sm group">
                                        <span className="bg-pink-100 text-pink-800 px-2 py-1 text-xs font-medium rounded-full mr-2 mb-2">@{follower.username}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </article>
                    <Divider />
                    <div>
                        <textarea
                            value={content}
                            onChange={(e) => setContent(e.target.value)}
                            placeholder="What's happening?"
                            style={{
                                border: '1px solid #ccc',
                                padding: '9px',
                                marginBottom: '10px',
                                marginLeft: '15px',
                                marginTop: '25px',
                                borderRadius: '15px',
                                width: '95%'
                            }}
                        />
                        <select
                            value={replyTo}
                            onChange={(e) => setReplyTo(e.target.value)}
                            style={{
                                border: '1px solid #ccc',
                                padding: '9px',
                                marginBottom: '10px',
                                marginLeft: '15px',
                                borderRadius: '15px',
                                width: '96%',
                                backgroundColor: '#f9f9f9',
                                cursor: 'pointer',
                                fontSize: '14px'
                            }}
                        >
                            <option value="">Select reply to</option>
                            {posts.map(post => (
                                <option key={post.id} value={post.id} style={{ padding: '9px', backgroundColor: '#fff', cursor: 'pointer' }}>
                                    {post.content}
                                </option>
                            ))}
                        </select>
                        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <button
                                onClick={handlePublish}
                                style={{
                                    backgroundColor: '#1DA1F2',
                                    color: 'white',
                                    fontWeight: 'bold',
                                    border: 'none',
                                    padding: '7px 15px',
                                    borderRadius: '15px',
                                    marginRight: '10px',
                                    marginBottom: '10px',
                                    cursor: 'pointer',
                                }}
                            >
                                Publish
                            </button>
                        </div>
                    </div>
                    <Divider />
                    {posts && posts.length > 0 && posts.map(post => (
                        <div key={post.id} className="flex space-x-3 border-b border-gray-extraLight px-4 py-3 cursor-pointer">
                            <div className="flex-shrink-0">
                                <img src={userImages[post.owner.id] || profile} alt="Profile" className="rounded-full w-12 h-12" />
                            </div>
                            <div className="flex-grow-1">
                                <div className="flex justify-between items-center text-sm mb-2">
                                    <span className="ml-2 text-gray-dark">@{post.owner.username}</span>
                                    <div className="mx-2 bg-gray-dark h-1 w-1 border rounded-full" />
                                    <span className="text-gray-dark">
                                        {post.created_at ? new Date(post.created_at).toLocaleString("tr-TR") : ""}
                                    </span>
                                </div>
                                {post.reply_to && (
                                    <div className="bg-gray-100 p-3 rounded mb-2">
                                        <div className="text-sm text-gray-700">Replying to:</div>
                                        <div className="text-sm text-gray-900 font-semibold">{getPostContentById(post.reply_to)}</div>
                                    </div>
                                )}
                                <p className="mb-2">{post.content}</p>
                                <div className="flex items-center">
                                    {likedPosts.includes(post.id) ? (
                                        <HeartFill className="text-danger cursor-pointer" onClick={() => handleLike(post.id)} />
                                    ) : (
                                        <Heart className="text-secondary cursor-pointer" onClick={() => handleLike(post.id)} />
                                    )}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
            <Modal open={openModal} onClose={handleCloseModal}>
                <Box sx={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', width: 400, bgcolor: 'background.paper', boxShadow: 24, p: 4 }}>
                    <h2>Edit Page</h2>
                    <TextField
                        fullWidth
                        margin="normal"
                        label="Title"
                        value={newTitle}
                        onChange={(e) => setNewTitle(e.target.value)}
                    />
                    <TextField
                        fullWidth
                        margin="normal"
                        label="Description"
                        value={newDescription}
                        onChange={(e) => setNewDescription(e.target.value)}
                    />
                    <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                        <Button variant="contained" color="primary" onClick={handleSaveChanges}>
                            Save
                        </Button>
                    </Box>
                </Box>
            </Modal>
        </>
    );
};

export default Tweet;
