import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:5000/'
const my_axios = axios.create({
  baseURL: BASE_URL,
  timeout: 50000
})

export default my_axios
