<script setup>
import { ref } from "vue"
import { v_required, v_length2 } from "@/composables/validators"
import ProgressLoading from "@/components/ProgressLoading.vue"
import SnackbarMessage from "@/components/SnackbarMessage.vue"

// communication
const emit = defineEmits(["changeStep", "updateRegistration"])
defineExpose({ setup })
const { $backend } = useNuxtApp()

//  snackbar and loading widgets
const refsnackbar = ref(null)
let showSnackbar
const refloading = ref(null)
let showLoading

// datamodel member
const birthyear = ref(0)
const category = ref("open")
const chesstitle = ref("")
const emailplayer = ref("")
const first_name = ref("")
const idbel = ref("")
const idfide = ref("")
const idsub = ref("")
const last_name = ref("")
const mobileplayer = ref("")
const nationalityfide = ref("")
const playerremark = ref("")

// datamodel the rest
const step = 3
const formvalid = ref(false)

async function next() {
  let reply
  showLoading(true)
  try {
    reply = await $backend("registration", "create_registration", {
      registrationIn: {
        category: category.value,
        emailplayer: emailplayer.value,
        idbel: idbel.value,
        idfide: idfide.value,
        idsub: idsub.value,
        locale: "en",
        mobileplayer: mobileplayer.value,
      },
    })
  } catch (error) {
    console.error("error", error)
    showSnackbar(error.message)
    return
  } finally {
    showLoading(false)
  }
  idsub.value = reply.data
  updateRegistration()
  emit("changeStep", step + 1)
}

function prev() {
  updateRegistration()
  emit("changeStep", step - 1)
}

function setup(e) {
  console.log("setup details", e)
  birthyear.value = e.birthyear
  category.value = e.category ? e.category : category.value
  chesstitle.value = e.chesstitle
  emailplayer.value = e.emailplayer
  first_name.value = e.first_name
  idbel.value = e.idbel
  idfide.value = e.idfide
  idsub.value = e.idsub
  last_name.value = e.last_name
  mobileplayer.value = e.mobileplayer
  nationalityfide.value = e.nationalityfide
  playerremark.value = e.playerremark
}

function updateRegistration() {
  emit("updateRegistration", {
    category: category.value,
    emailplayer: emailplayer.value,
    idsub: idsub.value,
    mobileplayer: mobileplayer.value,
  })
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar
  showLoading = refloading.value.showLoading
  category.value = "open"
})
</script>
<template>
  <v-form v-model="formvalid">
    <v-container>
      <SnackbarMessage ref="refsnackbar" />
      <ProgressLoading ref="refloading" />
      <v-row class="mt-2">
        <h2>Details registration</h2>
      </v-row>
      <v-row>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            First name: <b>{{ first_name }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            Last name: <b>{{ last_name }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            Birthyear: <b>{{ birthyear }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            FIDE nationality: <b>{{ nationalityfide }}</b>
          </div>
        </v-col>
        <v-col cols="12" md="6" class="pa-1">
          <div>
            Chess title: <b>{{ chesstitle }}</b>
          </div>
        </v-col>
      </v-row>
      <v-row>
        <h3 class="my-2">Required information</h3>
      </v-row>
      <v-row>
        <div class="my-2">Please provide the following details</div>
      </v-row>
      <v-row>
        <h4 class="mt-2 mb-1">Select tournament</h4>
      </v-row>
      <v-row class="mt-1">
        <VRadioGroup v-model="category" :rules="[v_required]">
          <VRadio label="Cocoon Open" value="open"></VRadio>
          <VRadio label="Cocoon -1800" value="m1800"></VRadio>
          <VRadio label="Cocoon Senior" value="sen"></VRadio>
        </VRadioGroup>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <VTextField
            label="Email"
            v-model="emailplayer"
            :rules="[v_required, v_length2]"
          />
        </v-col>
        <v-col cols="12" md="6">
          <VTextField
            label="Mobile phone"
            v-model="mobileplayer"
            :rules="[v_required, v_length2]"
          />
        </v-col>
        <v-col cols="12" md="6">
          <VTextField label="Remarks" v-model="playerremark" />
        </v-col>
      </v-row>
      <v-row class="mt-4">
        <div class="mt-2">
          <v-btn class="ml-2" @click="prev" color="primary"> Back </v-btn>
          <v-btn :disabled="!formvalid" class="ml-2" color="primary" @click="next">
            Continue
          </v-btn>
        </div>
      </v-row>
    </v-container>
  </v-form>
</template>
