<script setup>
import { ref } from "vue"
const drawer = ref(false)
</script>

<template>
  <v-app>
    <VNavigationDrawer v-model="drawer" class="bg-indigo-darken-1" dark>
      <v-toolbar dark text class="bg-indigo">
        <v-list>
          <v-list-item title="Menu" />
        </v-list>
      </v-toolbar>
      <v-list nav class="bm-blue-grey-darken-1">
        <v-list-item to="/" title="Home" />
        <v-list-group no-action>
          <template #activator="{ props }">
            <v-list-item v-bind="props" title="Cocoon" />
          </template>
          <v-list-item to="open" title="Open Tournament" />
          <v-list-item to="m1800" title="-1800 Tournament" />
          <v-list-item to="senior" title="Senior Tournament" />
          <v-list-item to="live" title="Live Games" />
          <v-list-item to="playing-schedule" title="Playing schedule" />
          <v-list-item href="/img/Cocoon2025.pdf" title="Brochure" />
          <v-list-item to="rules" title="Tournament Rules" />
        </v-list-group>
        <v-list-group no-action>
          <template #activator="{ props }">
            <v-list-item v-bind="props" title="Ostend" />
          </template>
          <v-list-item to="venue" title="Venue" />
          <v-list-item to="stay" title="Stay" />
        </v-list-group>
        <v-list-item to="activities" title="Side activities" />
        <v-list-item to="sponsors" title="Sponsors" />
      </v-list>
    </VNavigationDrawer>
    <v-app-bar color="indigo-darken-1">
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-app-bar-title> Cocoon </v-app-bar-title>
    </v-app-bar>
    <v-main>
      <slot />
      <hr />
      <div align="center" justify="center">
        <h4>Gold Sponsor</h4>
        <img src="/img/frame_oostende.png" alt="Gold Sponsor" />
      </div>
      <hr />
      <AdCarousel />
    </v-main>

    <TheFooter />
  </v-app>
</template>

<style scoped>
a:link,
a:hover {
  text-decoration: none;
}

.v-list-group--active.primary--text {
  color: white !important;
}
</style>
