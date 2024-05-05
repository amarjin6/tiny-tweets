import React, {useState} from "react";
import TweetService from "../service/TweetService";
import {useSelector} from "react-redux";
import Box from "./Box";

const TweetBox = ({refresh}) => {
    const [content, setContent] = useState("");
    const accessToken = useSelector(state => state.reduxSlice.accessToken)

    let config = {
        headers: {
            'Authorization': 'Bearer ' + accessToken
        }
     }

    const sendTweet = (tweet) => {
        let tweetService = new TweetService()
        tweetService.sendTweet(tweet, config).then(() => refresh())
    };

    const [title, setTitle] = useState('');
    const [tags, setTags] = useState([]);
    const [description, setDescription] = useState('');
    const [image, setImage] = useState('');
    const [expanded, setExpanded] = useState(false);
    const [isPrivate, setIsPrivate] = useState(false);

    const handleTagChange = (e, index) => {
        const newTags = [...tags];
        newTags[index] = e.target.value;
        setTags(newTags);
    };

    const addTagInput = () => {
        setTags([...tags, '']);
    };

    const handlePublish = () => {
        const tweet = {
          title,
          tags,
          description,
          image,
          is_private: isPrivate,
        };
        sendTweet(tweet);
        // Reset form fields
        setTitle('');
        setTags([]);
        setDescription('');
        setImage('');
        setIsPrivate(false);
        setExpanded(false);
    };
    return (
    <div>
      <textarea
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="What's happening?"
        onFocus={() => setExpanded(true)}
        style={{
          border: '1px solid #ccc',
          padding: '9px',
          marginBottom: '10px',
          borderRadius: '15px',
          width: '100%'
        }}
      />
      {expanded && (
        <>
          {tags.map((tag, index) => (
            <input
              key={index}
              type="text"
              value={tag}
              onChange={(e) => handleTagChange(e, index)}
              placeholder="Tag"
              style={{
                border: '1px solid #ccc',
                padding: '10px',
                marginBottom: '10px',
                borderRadius: '15px',
                width: '100%',
              }}
            />
          ))}
          <button
            onClick={addTagInput}
            style={{
              backgroundColor: '#1DA1F2',
              color: 'white',
              border: 'none',
              fontWeight: 'bold',
              padding: '7px 15px',
              borderRadius: '15px',
              marginBottom: '10px',
              cursor: 'pointer',
            }}
          >
            Add Tag
          </button>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description"
            style={{
              border: '1px solid #ccc',
              padding: '8px',
              marginBottom: '10px',
              borderRadius: '15px',
              width: '100%',
            }}
          />
          <input
            value={image}
            onChange={(e) => setImage(e.target.value)}
            placeholder="Image"
            style={{
              border: '1px solid #ccc',
              padding: '10px',
              marginBottom: '10px',
              borderRadius: '15px',
              width: '100%',
            }}
          />
          <div style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
            <input
              type="checkbox"
              checked={isPrivate}
              onChange={() => setIsPrivate(!isPrivate)}
              style={{ marginRight: '5px' }}
            />
            <label>Private</label>
          </div>
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
                  marginBottom: '10px',
                  cursor: 'pointer',
                }}
              >
                Publish
              </button>
          </div>
        </>
      )}
    </div>
  );
};

export default TweetBox;
