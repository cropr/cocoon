<script setup>
import { ref, computed } from "vue";
import ProgressLoading from "@/components/ProgressLoading.vue";
import SnackbarMessage from "@/components/SnackbarMessage.vue";

const runtimeConfig = useRuntimeConfig();

// communication
const emit = defineEmits(["changeStep", "restart"]);
defineExpose({ setup });
const { $backend } = useNuxtApp();

//  snackbar and loading widgets
const refsnackbar = ref(null);
let showSnackbar;
const refloading = ref(null);
let showLoading;

// datamodel member
const birthyear = ref(null);
const category = ref("");
const first_name = ref("");
const gender = ref(null);
const idsub = ref("");
const last_name = ref("");
const nationalityfide = ref("");
const photourl = computed(
  () => `${runtimeConfig.public.apiUrl}api/v1/registration/photo/${idsub.value}`
);
const isConfirmed = ref(false);

const step = 6;

async function confirm() {
  let reply;
  showLoading(true);
  try {
    reply = await $backend("registration", "confirm_registration", {
      idsub: idsub.value,
    });
  } catch (error) {
    console.error("confirmation failed", error);
    showSnackbar("Confirmation failed");
    return;
  } finally {
    showLoading(false);
  }
  isConfirmed.value = true;
}

function prev() {
  emit("changeStep", step - 1);
}

function restart() {
  isConfirmed.value = false;
  emit("restart");
}

function setup(e) {
  console.log("setup confirmation", e);
  birthyear.value = e.birthyear;
  category.value = e.category;
  gender.value = e.gender;
  idsub.value = e.idsub;
  first_name.value = e.first_name;
  nationalityfide.value = e.nationalityfide;
  last_name.value = e.last_name;
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar;
  showLoading = refloading.value.showLoading;
});
</script>
<template>
  <v-container>
    <SnackbarMessage ref="refsnackbar" />
    <ProgressLoading ref="refloading" />
    <v-row class="my-2">
      <h2>Confirmation</h2>
    </v-row>
    <v-row>
      <v-col cols="12" sm="4" lg="3">
        <v-img :src="photourl" width="160" />
      </v-col>
      <v-col cols="12" sm="4" lg="3">
        <div>
          Full name: <b>{{ last_name }}, {{ first_name }}</b>
        </div>
        <div>
          Birthyear: <b>{{ birthyear }}</b>
        </div>
        <div>
          FIDE nationality: <b>{{ nationalityfide }}</b>
        </div>
        <div>
          Gender: <b>{{ gender }}</b>
        </div>
        <div>
          Tournament: <b>{{ category }}</b>
        </div>
      </v-col>
    </v-row>
    <v-row class="my-4" v-show="!isConfirmed">
      <v-btn class="ml-2" @click="prev" color="primary"> Back </v-btn>
      <v-btn class="ml-2" @click="confirm" color="primary"> Confirm </v-btn>
    </v-row>
    <v-row class="my-2" v-show="isConfirmed">
      <v-alert text="Registration confirmed" type="success" />
    </v-row>
    <hr />
    <v-row v-show="isConfirmed" class="my-4">
      <h3>Payment</h3>
    </v-row>
    <v-row v-show="isConfirmed" class="my-4">
      <b>Do not pay yet.</b> We will send you in a separate email the detailed payment
      instructions.
    </v-row>
    <hr />
    <v-row v-show="isConfirmed" class="mt-6">
      <v-btn class="ml-2" @click="restart"> New registration </v-btn>
    </v-row>
  </v-container>
</template>
