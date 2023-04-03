<template>
  <div class="config">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <ConfigElection msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import ConfigElection from '@/components/ConfigElection.vue'

export default {
  name: 'ConfigView',
  components: {
    ConfigElection
  }
}
</script>

<style>
/* .config{
  margin-top: 50px;
} */
</style>
