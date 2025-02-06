import axios from "axios"

const prefix = "/api/v1/participant"

export default {
  get_participants: async function (options) {
    const { enabled } = options
    if (enabled) {
      return await axios.get(`${prefix}/list?enabled=1`)
    } else {
      return await axios.get(`${prefix}/list`)
    }
  },
  mgmt_import_registrations: async function (options) {
    const { token } = options
    return await axios.post(
      `${prefix}/import_registrations`,
      {},
      {
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    )
  },
  mgmt_get_participant: async function (options) {
    const { id, token } = options
    return await axios.get(`${prefix}/single/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_update_participant_bjk: async function (options) {
    const { id, participant, token } = options
    return await axios.put(`${prefix}/single/${id}`, participant, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  upload_photo_bjk: async function (options) {
    const { id, photo } = options
    return await axios.post(`${prefix}/photo/${id}`, { photo })
  },
}
