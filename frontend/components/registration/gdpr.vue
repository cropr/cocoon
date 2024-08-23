<script setup>
import { ref } from "vue";

// communication with main tool page
const emit = defineEmits(["changeStep"]);
defineExpose({ setup });

// datamodel
const gdpr_ok = ref("gdpr_ok");
const step = 5;

function next() {
  console.log("clicked next");
  emit("changeStep", step + 1);
}

function prev() {
  console.log("clicked prev");
  emit("changeStep", step - 1);
}

function setup(l) {
  console.log("setup gdpr", l);
}
</script>
<template>
  <v-container>
    <v-row>
      <h2>GDPR rules</h2>
    </v-row>
    <v-row>
      <div class="mt-2">
        <ul>
          <li>
            You authorize KOSK to use you personal data collected in this registration
            form
          </li>
          <li>KOSK will use the data for tournament purposes only</li>
          <li>
            KOSK will use the profile picture for your player badge and for identification
            on the website
          </li>
          <li>
            In any case KOSK will not leak any personal information to third parties.
          </li>
          <li>
            KOSK is taking overview photos/videos of the tournament and can publish these
            photos/videos on its website and on social media
          </li>
          <li>
            If KOSK is taking a close-up photos/video of a player, KOSK will explicitly
            ask permission to publish
          </li>
        </ul>
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        <VCheckbox label="Noted" v-model="gdpr_ok" />
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        <v-btn class="ml-2" @click="prev" color="primary"> Back </v-btn>
        <v-btn :disabled="!gdpr_ok" class="ml-2" color="primary" @click="next">
          Continue
        </v-btn>
      </div>
    </v-row>
  </v-container>
</template>
