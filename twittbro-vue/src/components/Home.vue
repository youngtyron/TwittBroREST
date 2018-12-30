<template>
  <mu-container>
    <mu-appbar color='primary'  class="navbar">

      TwittBro

      <mu-button flat slot='right' v-if='!auth' @click='goLogin'>Вход</mu-button>
      <mu-button flat slot='right' v-else @click='logout'>Выход</mu-button>
    </mu-appbar>
    <mu-bottom-nav v-if='auth'>

      <mu-button flat color="primary" @click="goToNews">Новости</mu-button>
      <mu-button flat color="primary" @click="goToMyWall">Моя страница</mu-button>
      <mu-button flat color="primary" @click="goToFollows">Мои подписки</mu-button>
      <!-- <mu-button flat color="primary" @click="goToMessenger">Мои сообщения<mu-badge v-if='unread' v-bind:content='String(unread)' circle color="secondary"  class="demo-icon-badge"></mu-badge></mu-button> -->
      <mu-button flat color="primary" @click="goToMessenger">Мои сообщения<mu-badge v-if='this.$root.unreadPinkMessages' v-bind:content='this.$root.unreadPinkMessages' circle color="secondary"  class="demo-icon-badge"></mu-badge></mu-button>
      <mu-button flat color="primary" @click="goToSearch">Поиск</mu-button>

    </mu-bottom-nav>
    <slot></slot>
  </mu-container>
</template>

<script>

  export default {
    name: 'Home',
    data() {
      return {
        unread: '',
      }
    },
    computed: {
      auth(){
        if (sessionStorage.getItem('auth_token')){
          return true
        }
      }
    },
    mounted(){
      // this.newUnread()
      this.$root.pinkMessagesFunc()
    },
    created(){
      setInterval(() => {
        // this.newUnread()
        this.$root.pinkMessagesFunc()
      }, 25000)
    },
    methods:{
      goLogin(){
        this.$router.push({name: 'login'})
      },
      logout() {
        sessionStorage.removeItem('auth_token')
        window.location = '/'
      },
      // newUnread(){
      //   $.ajax({
      //      url: 'http://127.0.0.1:8000/api/messenger/unread/',
      //      type: "GET",
      //      success: (response) => {
      //          this.unread =  response.data.data
      //        }
      //   })
      // },
      goToSearch(){
        this.$router.push({name: 'search'})
        // , params: {text: ''}
      },
      goToNews(){
        this.$router.push({name: 'news'})
      },
      goToMyWall(){
        this.$router.push({name: 'mywall'})
      },
      goToFollows(){
        this.$router.push({name: 'follows'})
      },
      goToMessenger(){
        this.$router.push({name: 'messenger'})
      },
    },
  }
</script>

<style scoped>
  .search-field{
    float: left;
    margin-left: 5px;
  }
  .fa-search{
    margin-top: 15px;
    float: left;
  }
  .navbar{
    width: 100%;
  }
</style>
