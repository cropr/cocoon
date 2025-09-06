<script setup></script>

<template>
  <SnackbarMessage ref="refsnackbar" />
  <ProgressLoading ref="refloading" />
  <v-container>
    <h1>-1800 Tournament</h1>
    <div>
      The pairings and results are available on
      <a href="https://chess-results.com/fed.aspx?lan=1&fed=BEL">ChessResults</a>.
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
