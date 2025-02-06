<script setup>
import { ref } from "vue"

const router = useRouter()
const drawer = ref(false)

async function goto(section) {
  const url = `/mgmt/${section}`
  router.push(url)
}

useHead({
  script: [{ src: "https://accounts.google.com/gsi/client", defer: true }],
})
</script>
<script></script>
<template>
  <VApp>
    <VNavigationDrawer v-model="drawer" color="deep-purple darken-1" dark>
      <VToolbar title="Cocoon Mgmt" color="deep-purple darken-3" dark />
      <v-list>
        <v-list-item @click="goto('overview')" title="Overview" />
        <v-list-item @click="goto('pages')" title="Pages" />
        <v-list-item @click="goto('paymentrequests')" title="Payment Requests" />
        <v-list-item @click="goto('registrations')" title="Registrations" />
        <v-list-item @click="goto('participants')" title="Participants" />
        <v-list-item @click="goto('logout')" title="Logout" />
      </v-list>
    </VNavigationDrawer>
    <VAppBar color="deep-purple darken-1" dark>
      <VAppBarNavIcon @click="drawer = !drawer" />
      <VAppBarTitle>Management Cocoon Website </VAppBarTitle>
    </VAppBar>
    <VMain>
      <slot />
    </VMain>
  </VApp>
</template>
