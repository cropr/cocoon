<script setup>
import { ref } from "vue"

const items = [
  { src: "/img/vanessa.jpg", name: "vanesa" },
  { src: "/img/frame_talistro.png", name: "talistro" },
  { src: "/img/frame_kbc.png", name: "kbc" },
  { src: "/img/frame_bnpparibas.png", name: "bnpparibas" },
]
const current = ref(Math.floor(Math.random() * items.length))

console.log("AdCarousel current", current.value)
</script>

<template>
  <div class="my-2">
    <v-carousel
      :show-arrows="false"
      hide-delimiters
      v-model="current"
      height="170"
      class="adcarousel mb-2"
      interval="5000"
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
