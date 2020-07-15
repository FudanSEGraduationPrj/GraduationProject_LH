<template>
  <p>Blank</p>
</template>

<script>
export default {
  name: 'Blank',
  data () {
    var words = this.$route.params.words
    this.$router.replace('/search/' + words)
    return {

    }
  },
  created () {

  }
}
</script>

<style scoped>

</style>
