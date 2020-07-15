<template>
  <div>
    <header id="search-header">
      <p id="logo" @click="toHome">
        <span class="logo-a">A</span>
        <span class="logo-p">P</span>
        <span class="logo-i">I</span>
        <span class="logo-e">E</span>
        <span class="logo-e">E</span>
      </p>
      <div id="search-box">
        <input id="search-box-input" ref="input" @keyup.enter="search">
        <button id ="search-icon"  @click="search"></button>
      </div>
    </header>
    <div id="content">
      <div id="results">
        <div v-for="(item, index) in dataShow" v-bind:key="index" @click="browseDescription(item)">
          <p class="keyword">
            {{ item.keyword }}
          </p>
          <p class="des">
            {{item.description}}
          </p>
        </div>
        <Page id="page" :total="total" :page-size="pageSize" show-elevator show-total @on-change="pageIndexChange"/>
      </div>
      <aside id="hot-words">
        <p class="title">
          <img src="../assets/fire.svg" width="24" height="24"/>
          <span>热词</span>
        </p>
        <ul>
          <li v-for="item in hotWords" v-bind:key="item.text">
            <div class="text">
              {{ item.text }}
            </div>
            <div class="degree">
              热度 {{ item.degree }}
            </div>
          </li>
        </ul>
      </aside>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Search',
  data () {
    return {
      results: [],
      hotWords: [],
      currentPage: 0,
      total: 8,
      pageSize: 10
    }
  },
  methods: {
    pageIndexChange (i) {
      this.$data.currentPage = i - 1
    },

    browseDescription (item) {
      this.$router.push({
        name: 'Description',
        params: {
          keyword: item.keyword,
          des: item.description
        }
      })
    },

    search () {
      var words = this.$refs.input.value
      if (words === '') {
        words = 'Java'
      }
      this.$http.post('http://175.24.14.65:5000/hotword/degree/inc/' + words).then(function () {
        // do nothing
      })
      this.$router.replace('/blank/' + words)
    },

    toHome () {
      this.$router.push('/')
    }
  },
  computed: {
    dataShow: function () {
      var start = this.$data.currentPage * this.$data.pageSize
      var end = Math.min((this.$data.currentPage + 1) * this.$data.pageSize, this.$data.results.length)
      return this.$data.results.slice(start, end)
    }
  },
  beforeCreate () {
    // var words = this.$route.params.words
  },
  created () {
    var words = this.$route.params.words
    this.$http.get('http://175.24.14.65:5000/search/' + words).then(function (result) {
      this.$data.results = result.body.results
      this.$data.total = this.$data.results.length
    })
    this.$http.get('http://175.24.14.65:5000/hotword/all').then(function (result) {
      this.$data.hotWords = result.body.hotwords
    })
  }
}
</script>

<style scoped>
/* header css */
#search-header {
  padding-top: 16px;
  padding-bottom: 24px;
  border-bottom: 1px solid rgb(233, 233, 233);
  min-width: 1060px;
  height: 85px;
}

#logo {
  height: 44px;
  width: 100px;
  position: absolute;
  text-align: center;
  display: inline-block;
  margin: 0;
  cursor: pointer;
}

.logo-a {
    color: #EA4335;
    font-size: 30px;
    font-weight: 400;
    display: inline-block;
    width: 15px;
}

.logo-p {
    color: #34A853;
    font-size: 30px;
    font-weight: 400;
    display: inline-block;
    width: 15px;
}

.logo-i {
    color: #4285F4;
    font-size: 30px;
    font-weight: 400;
    display: inline-block;
    width: 3px;
}

.logo-e {
    color: #FBBC05;
    font-size: 30px;
    font-weight: 400;
    display: inline-block;
    width: 14px;
}

#search-box {
  display: inline-block;
  background-color: white;
  cursor: text;
  margin: 0 auto 0 auto;
  width: 600px;
  box-shadow: 0 2px 5px 0 rgba(32, 33, 36, .28);
  border-radius: 22px;
  box-sizing: border-box;
  font-size: 16px;
  height: 44px;
  opacity: 1;
  position: absolute;
  left: 120px;
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

/* content css */
#content {
  display: flex;
  width: 1060px;
}

#results {
  display: block;
  width: 700px;
  margin-left: 120px;
  margin-right: 30px;
}

#hot-words {
  display: block;
  width: 200px;
}

#hot-words p {
  margin-top: 16px;
  margin-bottom: 8px;
}

#hot-words ul {
  padding-inline-start: 5px;
  list-style-type: none;
  margin: 0;
}

#hot-words ul li {
  margin-bottom: 12px;
}

#hot-words .text {
  font-size: 14px;
  margin-bottom: 4px;
  color: #666666;
}

#hot-words .degree {
  font-size: 12px;
  color: #969696;
}

#results .keyword {
  margin-top: 24px;
  font-size: 24px;
  color: rgb(26, 13, 171);
  cursor: pointer;
}

#results .des {
  padding-top: 6px;
  color: rgb(88, 88, 88);
  font-size: 16px;
  cursor: pointer;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

#results #page {
  margin-top: 16px;
  margin-bottom: 16px;
}
</style>
