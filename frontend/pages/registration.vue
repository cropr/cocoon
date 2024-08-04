<script setup>
import { ref, computed } from 'vue'


// communication with stepped children
const step = ref(1)
const refintro = ref(null)
const refidnumber = ref(null)
const refdetails = ref(null)
const refphoto = ref(null)
const refgdpr = ref(null)
const refconfirmation = ref(null)


// data model
const registration = ref({})

function changeStep(s) {
  console.log('receive update step', s)
  step.value = s
  switch (s) {
    case 1:
      refintro.value.setup(registration.value)
      break
    case 2:
      refidnumber.value.setup(registration.value)
      break
    case 3:
      refdetails.value.setup(registration.value)
      break
    case 4:
      refphoto.value.setup(registration.value)
      break
    case 5:
      refgdpr.value.setup(registration.value)
      break
    case 6:
      refconfirmation.value.setup(registration.value)
      break
  }
}

function updateRegistration(l) {
  console.log('receive update registration', l)
  Object.assign(registration.value, l)
}

function restart() {
  registration.value = {}
  step.value = 1
}

</script>

<template>
  <v-container fluid>
    <h1 class="my-2">Registration tool </h1>
    <div>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>1</v-chip>
          Intro
        </v-card-title>
        <v-card-text>
          <registrationIntro v-show="step == 1" ref="refintro" @change-step="changeStep" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>2</v-chip>
            ID number
        </v-card-title>
        <v-card-text>
          <registrationIdnumber v-show="step == 2" ref="refidnumber" @change-step="changeStep"
            @update-registration="updateRegistration" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>3</v-chip>
          Details
        </v-card-title>
        <v-card-text>
          <registrationDetails v-show="step == 3" ref="refdetails" @change-step="changeStep"
            @update-registration="updateRegistration" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>4</v-chip>
          Photo
        </v-card-title>
        <v-card-text v-show="step == 4">
          <registrationPhoto ref="refphoto" @change-step="changeStep"
            @update-registration="updateRegistration" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>5</v-chip>
          GDPR
        </v-card-title>
        <v-card-text>
          <registrationGdpr v-show="step == 5" ref="refgdpr" @change-step="changeStep"
            @update-registration="updateRegistration" />
        </v-card-text>
      </v-card>
      <v-card class="my-2">
        <v-card-title class="text-h5 py-2 mb-2 bottomline">
          <v-chip>6</v-chip>
          Confirmation
        </v-card-title>
        <v-card-text>
          <registrationConfirmation v-show="step == 6" ref="refconfirmation" @change-step="changeStep"
            @restart="restart" />
        </v-card-text>
      </v-card>
    </div>
  </v-container>
</template>

<style scoped>
.bottomline {
  border-bottom: 1px solid #aaa;
}
</style>