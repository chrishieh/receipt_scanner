
<template>
  <div id="app">
    <PictureUpload />
  </div>
</template>

<script>
import PictureUpload from "@/components/PictureUpload.vue";

export default {
  components: {
    PictureUpload,
  },
};
</script>

<style>
  body {
    background-color: #f8f8f8; /* Set your desired light background color */
    color: #333;
  }
</style>