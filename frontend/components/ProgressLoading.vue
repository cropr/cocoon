<script setup>

const visible = ref(false)
function showLoading(show) {
  visible.value = show
}

defineExpose({ showLoading })

</script>
<template>
  <VDialog v-model="visible" class="text-center" width="auto">
    <VCard>
      <VCardTitle class="mx-auto">
        Loading...
      </VCardTitle>
      <VCardText class="mx-auto">
        <VProgressCircular indeterminate color="green" />
      </VCardText>
    </VCard>
  </VDialog>
</template>