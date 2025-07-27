import axios from "axios"

const prefix = "/api/v1/wagtail"

export default {
  get_pages: async function (options) {
    return await axios.get(`${prefix}/pages/`)
  },
  get_page: async function (options) {
    const { slug } = options
    return await axios.get(`${prefix}/pages/${slug}`)
  },
  get_images: async function (options) {
    return await axios.get(`${prefix}/images/`)
  },
  get_image: async function (options) {
    const { title } = options
    return await axios.get(`${prefix}/images/${title}`)
  },
}
