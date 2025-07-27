<script setup>
import { ref } from "vue"

// communication
const { $backend } = useNuxtApp()

//snackbar progessloading
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

const pagetitle = ref("")
const pagecontent = ref("")
const pageintro = ref("")

async function getPage(slug) {
  console.log("getPage", slug)
  showLoading(true)
  try {
    let reply = await $backend("wagtail", "get_page", {
      slug: slug,
    })
    const page = reply.data
    console.log("page", page)
    pagetitle.value = page.title
    pageintro.value = page.intro
    pagecontent.value = page.body
  } catch (error) {
    showSnackbar("Page loading failed")
    console.log("getPage error", error)
  } finally {
    showLoading(false)
  }
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  getPage("stay")
})
</script>

<template>
  <SnackbarMessage ref="refsnackbar" />
  <ProgressLoading ref="refloading" />
  <v-container>
    <h1>{{ pagetitle }}</h1>
    <div>
      <i>{{ pageintro }}</i>
    </div>
    <div v-html="pagecontent"></div>
  </v-container>
</template>

<style scoped>
h1:after {
  content: " ";
  display: block;
  border: 1px solid #aaa;
  margin-bottom: 1em;
}

ul {
  padding-left: 1rem;
}
.v-card-title {
  white-space: normal;
}
.nopadding {
  padding: 0;
}
</style>
