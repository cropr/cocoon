<script setup>
import { ref } from "vue"

//snackbar progessloading
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

const { $cms } = useNuxtApp()
let pages = {}
const pagetitle = ref("")
const pagecontent = ref("")
const pageintro = ref("")

async function getPages() {
  console.log("getPages")
  showLoading(true)
  try {
    let reply = await $cms({
      method: "get",
      url: "/apiwt/pages",
    })
    pages = reply.data.items
  } catch (error) {
    showSnackbar("Page loading failed")
    console.log("getPages error", error)
    return
  } finally {
    showLoading(false)
  }
  await findPage("cocoon-2025")
}

async function getPage(id) {
  console.log("getPage", id)
  showLoading(true)
  try {
    let reply = await $cms({
      method: "get",
      url: `/apiwt/pages/${id}/`,
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

async function findPage(slug) {
  console.log("findPage", slug)
  let foundid = 0
  pages.forEach((page) => {
    if (page.meta.slug === slug) {
      foundid = page.id
    }
  })
  if (foundid) {
    await getPage(foundid)
  } else {
    showSnackbar("Page not found")
  }
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  getPages()
})
</script>

<template>
  <SnackbarMessage ref="refsnackbar" />
  <ProgressLoading ref="refloading" />
  <v-container fluid class="nopadding">
    <img width="100%" src="/img/landschap2.jpg" />
  </v-container>
  <v-container>
    <h1>{{ pagetitle }}</h1>
    <h3>{{ pageintro }}</h3>
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
