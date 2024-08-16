<script setup>
import { ref, onMounted } from "vue";
import * as jose from "jose";
import { usePersonStore } from "@/store/person";
import { storeToRefs } from "pinia";

// stores
const personstore = usePersonStore();
const { person } = storeToRefs(personstore);

// datamodel
const wrong_domain = ref(false);

async function checkAuth() {
  console.log("checking if auth is present so we can go to overview");
  if (person.value.credentials.length > 0) {
    if (person.value.email.endsWith("@kosk.be")) {
      navigateTo("/mgmt/overview");
    } else {
      wrong_domain.value = true;
    }
  }
}

function handleGoogle(resp) {
  console.log("handling google");
  wrong_domain.value = false;
  const payload = jose.decodeJwt(resp.credential);
  console.log("decoded", payload);
  personstore.updatePerson({
    credentials: resp.credential,
    user: payload.given_name,
    email: payload.email,
  });
  checkAuth();
}

function setupGoogle() {
  console.log("Setup google sign in");
  const reply = google.accounts.id.initialize({
    client_id: "899786740417-dhtk8pilvkhkne3ht3c6ecbnm0619ijm.apps.googleusercontent.com",
    callback: handleGoogle,
    prompt_parent_id: "parent_id",
  });
  console.log("initialize:", reply);
  const prompt = google.accounts.id.prompt((notif) => {
    console.log("notif", notif);
    if (notif.isNotDisplayed() || notif.isSkippedMoment()) {
      document.cookie = `g_state=;path=/;expires=Thu, 01 Jan 1970 00:00:01 GMT`;
      google.accounts.id.prompt();
    }
  });
  console.log("prompt", prompt);
  console.log("Setup google sign in completed");
}

useHead({
  title: "Management Login",
});

definePageMeta({
  layout: "mgmt",
});

onMounted(() => {
  checkAuth();
  setupGoogle();
});
</script>

<template>
  <VContainer>
    <p>Management Cocoon</p>
    <p>
      This part of the site is only accessible for people with a valid @kosk.be email
      address
    </p>
    <div id="parent_id" />
    <v-alert error v-show="wrong_domain">Invalid domain</v-alert>
  </VContainer>
</template>
