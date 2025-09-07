<script setup></script>

<template>
  <SnackbarMessage ref="refsnackbar" />
  <ProgressLoading ref="refloading" />
  <v-container>
    <h1>Open Tournament</h1>
    <div>
      The pairings and results are available on
      <a href="https://s2.chess-results.com/tnr1249960.aspx" target="_blank"
        >ChessResults</a
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
