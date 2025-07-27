import axios from "axios"

const prefix = "/api/v1/wagtail"

export default {
  wagtail_list: async function (options) {
    return await axios.get(`${prefix}/`)
  },
  wagtail_page: async function (options) {
    const { slug } = options
    return await axios.get(`${prefix}/${slug}/`)
  },
}
