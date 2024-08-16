<script setup>
import { ref, watch } from "vue";
import showdown from "showdown";

const mdConverter = new showdown.Converter();

const { $backend } = useNuxtApp();
let page;
const pagetitle = ref("");
const pagecontent = ref("");

async function getContent() {
  try {
    const reply = await $backend("filestore", "anon_get_file", {
      group: "pages",
      name: "venue.md",
    });
    page = useMarkdown(reply.data);
    console.log("page", page);
    pagetitle.value = page.metadata.title;
    pagecontent.value = page.html;
  } catch (error) {
    console.log("failed");
  }
}

onMounted(() => {
  getContent();
});
</script>

<template>
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
</style>
