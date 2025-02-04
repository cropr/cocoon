<script setup>
import { ref, watch } from "vue"
import showdown from "showdown"

//snackbar progessloading
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

const { $backend } = useNuxtApp()
let page
const pagetitle = ref("")
const pagecontent = ref("")

async function getContent() {
  showLoading(true)
  try {
    const reply = await $backend("filestore", "anon_get_file", {
      group: "pages",
      name: "cocoon.md",
    })
    page = useMarkdown(reply.data)
    pagetitle.value = page.metadata.title
    pagecontent.value = page.html
  } catch (error) {
    showSnackbar("Page loading failed")
  } finally {
    showLoading(false)
  }
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  getContent()
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
    <div v-html="pagecontent" class="markdowncontent"></div>
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
