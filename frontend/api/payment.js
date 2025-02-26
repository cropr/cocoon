import axios from "axios"

const prefix = "/api/v1/payment"

export default {
  mgmt_create_participant_pr: async function (options) {
    const { token, id } = options
    return await axios.post(
      `${prefix}/participant_pr/${id}`,
      {},
      {
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    )
  },
  mgmt_create_participants_pr: async function (options) {
    const { token } = options
    return await axios.post(
      `${prefix}/participant_pr`,
      {},
      {
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    )
  },
  mgmt_delete_participant_pr: async function (options) {
    const { token, id } = options
    return await axios.delete(`${prefix}/participant_pr/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_update_participant_pr: async function (options) {
    console.log("calling api update pr bjk", options)
    const { token, id, prq } = options
    return await axios.put(`${prefix}/participant_pr/${id}`, prq, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },

  // general
  mgmt_email_pr: async function (options) {
    const { token, id, prq } = options
    return await axios.post(`${prefix}/email_pr/${id}`, prq, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_email_prs: async function (options) {
    const { token, id, prq } = options
    return await axios.post(`${prefix}/email_pr`, null, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_get_paymentrequests: async function (options) {
    const { token } = options
    console.log("get_pra", token)
    return await axios.get(`${prefix}/pr`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
  mgmt_get_paymentrequest: async function (options) {
    const { token, id } = options
    return await axios.get(`${prefix}/pr/${id}`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
  },
}
