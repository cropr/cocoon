<script setup>
import { ref } from "vue"
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
import { useMgmtTokenStore } from "@/store/mgmttoken"
import { usePersonStore } from "@/store/person"
import { storeToRefs } from "pinia"

// communication
const { $backend } = useNuxtApp()
const router = useRouter()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// stores
const mgmtstore = useMgmtTokenStore()
const { token } = storeToRefs(mgmtstore)
const personstore = usePersonStore()
const { person } = storeToRefs(personstore)

// datamodel
const registrations = ref([])
const search = ref("")
const headers = [
  { title: "Last Name", value: "last_name" },
  { title: "First Name", value: "first_name" },
  { title: "Category", value: "category" },
  { title: "ID Bel", value: "idbel" },
  { title: "ID Fide", value: "idfide" },
  { title: "Comfirmed", value: "confirmed" },
  { title: "Actions", value: "action", sortable: false },
]
const itemsPerPage = 50
const itemsPerPageOptions = [
  { value: 50, title: "50" },
  { value: 150, title: "150" },
  { value: -1, title: "All" },
]

definePageMeta({
  layout: "mgmt",
})

async function checkAuth() {
  console.log("checking if auth is already set", token.value)
  if (token.value) return
  if (person.value.credentials.length === 0) {
    router.push("/mgmt")
    return
  }
  if (!person.value.email.endsWith("@kosk.be")) {
    router.push("/mgmt")
    return
  }
  let reply
  showLoading(true)
  // now login using the Google auth token
  try {
    reply = await $backend("accounts", "login", {
      logintype: "google",
      token: person.value.credentials,
      username: null,
      password: null,
    })
  } catch (error) {
    console.log("cannot login", error)
    router.push("/mgmt")
    return
  } finally {
    showLoading(false)
  }
  console.log("mgmttoken received", reply.data)
  mgmtstore.updateToken(reply.data)
}

async function editRegistration(item) {
  router.push("/mgmt/registration_edit?id=" + item.id)
}

async function getRegistrations() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("registration", "get_registrations")
    registrations.value = reply.data
    console.log("regs", registrations.value)
  } catch (error) {
    console.error("getting registrations failed", error)
    showSnackbar("Getting registrations failed")
    return
  } finally {
    showLoading(false)
  }
}

function gotoPaymentRequest(item) {
  router.push("/mgmt/paymentrequest_edit?id=" + item.payment_id)
}

function lightgreyRow(item) {
  if (!item.enabled) {
    return "lightgreyrow"
  }
}

async function refresh() {
  await getRegistrations()
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  await checkAuth()
  await getRegistrations()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>Management Registrations Cocoon 2025</h1>
    <v-data-table
      :headers="headers"
      :items="registrations"
      :item-class="lightgreyRow"
      :items-per-page="itemsPerPage"
      :items-per-page-options="itemsPerPageOptions"
      class="elevation-1"
      :sort-by="[{ key: 'last_name', order: 'asc' }]"
      :search="search"
    >
      <template #top>
        <v-card color="grey lighten-4">
          <v-card-title>
            <v-row class="px-2">
              <v-text-field
                v-model="search"
                label="Search"
                class="mx-4"
                append-icon="mdi-magnify"
                hide_details
              />
              <v-spacer />
              <v-tooltip location="bottom" text="Refresh">
                <template #activator="{ props }">
                  <v-btn
                    fab
                    outlined
                    color="deep-purple"
                    v-bind="props"
                    @click="refresh()"
                  >
                    <v-icon>mdi-refresh</v-icon>
                  </v-btn>
                </template>
              </v-tooltip>
            </v-row>
          </v-card-title>
        </v-card>
      </template>
      <template #item.payment_id="{ item }">
        <NuxtLink
          v-if="item.payment_id"
          :to="'/mgmt/paymentrequestedit?id=' + item.payment_id"
        >
          link
        </NuxtLink>
      </template>
      <template #item.action="{ item }">
        <v-tooltip bottom>
          Edit
          <template #activator="{ props }">
            <v-icon small class="mr-2" v-bind="props" @click="editRegistration(item)">
              mdi-pencil
            </v-icon>
          </template>
        </v-tooltip>
        <v-tooltip v-if="item.payment_id" bottom>
          <template #activator="{ on }">
            <v-icon small class="mr-2" v-on="on" @click="gotoPaymentRequest(item)">
              mdi-currency-eur
            </v-icon>
          </template>
          Show payment request
        </v-tooltip>
      </template>
      <template #no-data> No registrations found. </template>
    </v-data-table>
  </v-container>
</template>

<style scoped>
.disabled {
  color: rgb(186, 185, 185);
}
</style>
