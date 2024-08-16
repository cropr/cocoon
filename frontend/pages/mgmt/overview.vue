<script setup>
import { onMounted } from "vue";
import { usePersonStore } from "@/store/person";
import { storeToRefs } from "pinia";

const config = useRuntimeConfig();
const personstore = usePersonStore();
const { person } = storeToRefs(personstore);

definePageMeta({
  layout: "mgmt",
});

useHead({
  title: "Management Overview",
});

function checkAuth() {
  if (person.value.credentials.length === 0) {
    navigateTo("/mgmt");
  }
  if (!person.value.email.endsWith("@kosk.be")) {
    navigateTo("/mgmt");
  }
}

onMounted(() => {
  checkAuth();
});
</script>

<template>
  <v-container class="markdowncontent">
    <h1>Overview</h1>
    <ul>
      <li>Managing the <NuxtLink to="/mgmt/pages">Pages</NuxtLink></li>
      <!-- <li>Managing the <NuxtLink to="/mgmt/paymentrequests">Payment Requests</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/registrations">Registrations</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/participants">Participants</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/tournament">Tournaments</NuxtLink>
      </li>
      <li>Managing the <NuxtLink to="/mgmt/attendees">Attendees</NuxtLink> -->
      <!-- </li> -->
    </ul>
  </v-container>
</template>
