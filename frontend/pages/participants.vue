<script setup>
import { ref } from "vue"
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"

// communication
const { $backend } = useNuxtApp()
const router = useRouter()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// datamodel
const participants = ref([])
const search = ref("")
const headers = [
  { title: "N", value: "index" },
  { title: "Title", value: "chesstitle", sortable: true },
  { title: "Last Name", value: "last_name", sortable: true },
  { title: "First Name", value: "first_name", sortable: true },
  { title: "Elo FIDE", value: "ratingfide", sortable: true },
  { title: "Nationality", value: "nationalityfide", sortable: true },
  { title: "Category", value: "category", sortable: true },
]

async function getParticipants() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("participant", "get_participants", { enabled: 1 })
    participants.value = reply.data
  } catch (error) {
    console.error("getting participants failed", error)
    showSnackbar("Getting participants failed")
    return
  } finally {
    showLoading(false)
  }
}

onMounted(async () => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  console.log("aha")
  await getParticipants()
})
</script>

<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <h1>Participants Cocoon 2025</h1>
    <v-data-table
      :headers="headers"
      :items="participants"
      :item-class="lightgreyRow"
      :items-per-page-options="[150, -1]"
      items-per-page="150"
      class="elevation-1"
      :sort-by="[{ key: 'last_name', order: 'asc' }]"
      :search="search"
      density="compact"
    >
      <template #top>
        <v-card color="bg-grey-lighten-4">
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
            </v-row>
          </v-card-title>
        </v-card>
      </template>
      <template v-slot:item.index="{ index }">
        <span>
          {{ index + 1 }}
        </span>
      </template>

      <template #no-data> No participants found. </template>
    </v-data-table>
  </v-container>
</template>
