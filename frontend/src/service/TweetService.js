import axios from 'axios'

export default class TweetService {

    getTweets(config) {
        return axios.get('/api/v1/pages', config)
    }

    getTweetById(id) {
        return axios.get("/api/v1/pages/" + id);
    }

    sendTweet(body) {
        return axios.post("/api/v1/pages/", body)
    }

    getTweetsCommentByTweetId(id) {
        return axios.get((`/tweets/${id}/comments`))
    }
}