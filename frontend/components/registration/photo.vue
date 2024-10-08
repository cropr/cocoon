<script setup>
import { ref, computed } from "vue";
import VueCropper from "vue-cropperjs";
import "cropperjs/dist/cropper.css";
import ProgressLoading from "@/components/ProgressLoading.vue";
import SnackbarMessage from "@/components/SnackbarMessage.vue";

// communication
const emit = defineEmits(["changeStep", "updateRegistration"]);
defineExpose({ setup });
const { $backend } = useNuxtApp();

//  snackbar and loading widgets
const refsnackbar = ref(null);
let showSnackbar;
const refloading = ref(null);
let showLoading;

// datamodel member
const first_name = ref("");
const last_name = ref("");
const idsub = ref("");
const photo = ref(null);
const photosrc = ref(null);

// datamodel the rest
const step = 4;
async function uploadPhoto() {
  let reply;
  showLoading(true);
  photo.value = photosrc.value.getCroppedCanvas({ width: 160 }).toDataURL();
  try {
    reply = await $backend("registration", "upload_photo", {
      photo: photo.value,
      idsub: idsub.value,
    });
    emit("changeStep", step + 1);
  } catch (error) {
    showSnackbar(error.message);
  } finally {
    showLoading(false);
  }
}

function handleFile(event) {
  console.log("handleFile event fired", event);
  const reader = new FileReader();
  console.log("reader object created", reader);
  reader.onload = (event) => {
    console.log("onload event fired", event);
    photosrc.value.replace(event.target.result);
  };
  console.log("trying to read the the data url");
  reader.readAsDataURL(event);
}

function next() {
  uploadPhoto();
}

function prev() {
  emit("changeStep", step - 1);
}

function setup(e) {
  first_name.value = e.first_name;
  last_name.value = e.last_name;
  idsub.value = e.idsub;
}

function updateRegistration() {
  emit("updateRegistration", {});
}

onMounted(() => {
  showSnackbar = refsnackbar.value.showSnackbar;
  showLoading = refloading.value.showLoading;
});
</script>
<template>
  <v-form>
    <v-container>
      <SnackbarMessage ref="refsnackbar" />
      <ProgressLoading ref="refloading" />
      <v-row class="mt-2">
        <h2>Photo}</h2>
      </v-row>
      <v-row class="my-2">
        <div class="my-2">We need a photo to make your tournament badge.</div>
      </v-row>
      <v-row class="my-2">
        <v-col cols="12">
          <div class="my-2">
            You need to select a photo by clicking the photo icon and selecting a photo to
            upload.
          </div>
        </v-col>
        <v-col cols="12">
          <v-file-input label="Badge" v-model="photo" @update:modelValue="handleFile" />
        </v-col>
      </v-row>
      <v-row class="my-2">
        <v-col cols="12">
          <div>
            Once the photo is selected, you can move the selector handles with your mouse
            in order to adjust the photo. Please make sure that the face of player fills
            the resulting image. When the resulting image seems OK, click continue.
          </div>
        </v-col>
        <vue-cropper
          ref="photosrc"
          :view-mode="2"
          drag-mode="crop"
          :auto-crop-area="0.5"
          :background="true"
          src=""
          alt=" "
          :aspect-ratio="0.8"
          preview="#photoresult"
          :img-style="{ height: '400px' }"
        />
      </v-row>
      <v-row class="my-2">
        <h4>Resulting Image</h4>
      </v-row>
      <v-row class="my-2">
        <div id="photoresult" ref="photoresult" class="photoresult" />
      </v-row>
      <v-row class="mt-4">
        <div>
          <v-btn class="ml-2" @click="prev" color="primary"> Back </v-btn>
          <v-btn class="ml-2" color="primary" @click="next"> Continue </v-btn>
        </div>
      </v-row>
    </v-container>
  </v-form>
</template>

<style>
.dropbox {
  width: 100%;
  background-color: aliceblue;
}

.photosrc {
  overflow: hidden;
  width: 100%;
  height: 400px;
  border: 1px dashed #808080;
  background-color: #d3d3d3;
}

.photoresult {
  overflow: hidden;
  position: relative;
  text-align: center;
  width: 160px;
  height: 200px;
}
</style>
