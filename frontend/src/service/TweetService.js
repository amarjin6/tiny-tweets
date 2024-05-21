import axios from 'axios'

export default class TweetService {

    getTweets(config) {
        return axios.get('/api/v1/pages', config)
    }

    getTweetById(id, config) {
        return axios.get("/api/v1/pages/" + id, config);
    }

    sendTweet(body, config) {
        return axios.post("/api/v1/pages/", body, config)
    }

    getTweetsCommentByTweetId(id, config) {
        return axios.get(`/api/v1/posts/`, config)
    }
}
