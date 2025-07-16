<script setup>
import { ref } from "vue"

const current = ref(0)
const interval = 6
const items = [
  { src: "/img/vanessa.jpg", name: "vanesa" },
  { src: "/img/frame_talistro.png", name: "talistro" },
  { src: "/img/frame_kbc.png", name: "kbc" },
  { src: "/img/frame_oostende.png", name: "oostende" },
  { src: "/img/frame_bnpparibas.png", name: "bnpparibas" },
]

function setupCarousel() {
  let secCarousel = Math.floor((new Date() / 1000) % (interval * items.length))
  current.value = Math.floor(secCarousel / items.length)
  if (current.value == items.length) current.value = 0
}

onMounted(() => setupCarousel())
</script>

<template>
  <div class="my-2">
    <v-carousel
      :show-arrows="false"
      hide-delimiters
      :value="current"
      height="170"
      class="adcarousel mb-2"
      :interval="interval * 1000"
      cycle
      continuous
    >
      <v-carousel-item v-for="item in items" :key="item.name" :src="item.src">
      </v-carousel-item>
    </v-carousel>
  </div>
</template>

<style scoped>
.adcarousel.v-carousel {
  width: 360px;
  max-width: 95%;
  margin-left: auto;
  margin-right: auto;
}
</style>
