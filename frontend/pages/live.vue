<script setup></script>

<template>
  <SnackbarMessage ref="refsnackbar" />
  <ProgressLoading ref="refloading" />
  <v-container>
    <h1>Live Games Open</h1>
    <div>
      The live games are available
      <a href="https://view.livechesscloud.com/#f379456e-bd49-4d8f-8a99-5fe8e6124282"
        >here</a
      >.
    </div>
  </v-container>
</template>

<style scoped>
h1:after {
  content: " ";
  display: block;
  border: 1px solid #aaa;
  margin-bottom: 1em;
}
</style>
