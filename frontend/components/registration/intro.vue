<script setup>
// communication with main tool page
const emit = defineEmits(["changeStep"])
defineExpose({ setup })

const step = 1

function next() {
  console.log("clicked next")
  emit("changeStep", step + 1)
}

function setup(l) {
  console.log("setup intro", l)
}
</script>
<template>
  <v-container>
    <v-row>
      <h2>Intro</h2>
    </v-row>
    <v-row>
      <div class="mt-2">
        In order to register for the Cocoon tournament, you need to provide the following
        elements:
        <ul>
          <li>your ID number from the Royal Belgian Chess Federation</li>
          <li>or, if you don't have a Belgian ID number, your FIDE ID number</li>
        </ul>
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        If you have no ID at all, please contact your chess club and they should help you
        out.
      </div>
    </v-row>
    <v-row>
      <div class="mt-2">
        <v-btn color="primary" @click="next"> Continue </v-btn>
      </div>
    </v-row>
  </v-container>
</template>
