<script setup>
import { ref } from "vue"

const router = useRouter()
const drawer = ref(false);

async function goto(section) {
  const url = `/mgmt/${section}`
  router.push(url)
}

useHead({
  script: [
    { src: 'https://accounts.google.com/gsi/client', defer: true }
  ],
})


</script>
<script>
</script>
<template>
  <VApp>
    <VNavigationDrawer v-model="drawer" color="deep-purple darken-1" dark>
      <VToolbar title="Cocoon Mgmt" color="deep-purple darken-3" dark />
      <v-list>
        <v-list-item @click="goto('overview')" title="Overview" />
        <v-list-item @click="goto('pages')" title="Pages" />
        <v-list-item @click="goto('paymentrequests')" title="Payment Requests" />
        <v-list-group no-action>
          <template #activator="{ props }">
            <v-list-item v-bind="props" title="Cocoon 2024" />
          </template>
          <v-list-item @click="goto('registrations_24')" title="Registrations" />
          <v-list-item @click="goto('participants_24')" title="Participants" />
          <v-list-item @click="goto('tournament_24')" title="Tournaments" />
          <v-list-item @click="goto('attendee_24')" title="Attendees" />
        </v-list-group>
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
