<template>
  <div>
    <div id="logo-container">
      <p class="logo-top-blank"></p>
      <p id="logo">
        <span class="logo-a">A</span>
        <span class="logo-p">P</span>
        <span class="logo-i">I</span>
        <span class="logo-e">E</span>
        <span class="logo-e">E</span>
      </p>
    </div>
    <div id="search-box-container">
      <div id="search-box">
        <input id="search-box-input" ref="input" @keyup.enter="search">
        <button id ="search-icon" @click="search"></button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Index',
  methods: {
    search () {
      var words = this.$refs.input.value
      if (words === '') {
        words = 'Java'
      }
      this.$http.post('http://175.24.14.65:5000/hotword/degree/inc/' + words).then(function () {
        // do nothing
      })
      this.$router.push('/search/' + words)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* logo css */
.logo-top-blank {
  height: 100px;
}

#logo {
  text-align: center;
  margin: 0;
}

.logo-a {
  color: #EA4335;
  font-size: 80px;
  font-weight: 400;
  display: inline-block;
  width: 60px;
}

.logo-p {
  color: #34A853;
  font-size: 80px;
  font-weight: 400;
  display: inline-block;
  width: 60px;
}

.logo-i {
  color: #4285F4;
  font-size: 80px;
  font-weight: 400;
  display: inline-block;
  width: 60px;
}

.logo-e {
  color: #FBBC05;
  font-size: 80px;
  font-weight: 400;
  display: inline-block;
  width: 60px;
}

/* search box css */
#search-box-container {
  margin: 0 auto 0 auto;
  min-width: 400px;
  width: var(--conten-width);
  --search-box-height: 44px;
}

#search-box {
  background-color: white;
  cursor: text;
  margin: 0 auto 0 auto;
  max-width: 560px;
  min-width: 320px;
  box-shadow: 0 2px 5px 0 rgba(32, 33, 36, .28);
  border-radius: 22px;
  box-sizing: border-box;
  font-size: 16px;
  height: var(--search-box-height);
  opacity: 1;
  position: relative;
}

#search-icon {
  top: 0;
  right: 8px;
  bottom: 0;
  position: absolute;
  width: 24px;
  height: 44px;
  border: 0;
  margin: 0;
  padding: 0;
  outline: none;
  cursor: pointer;
  background: url(../assets/search.svg) no-repeat center;
}

#search-box > input {
  top: 0;
  bottom: 0;
  left: 0;
  padding-inline-start: 16px;
  position: absolute;
  box-sizing: border-box;
  margin: 0;
  width: 90%;
  border: none;
  outline: none;
  background-color: transparent;
  font-size: 16px;
}
</style>
