<template>
  <mu-container>
    <mu-appbar color='primary'  class="navbar">
      <!-- <i v-if='auth' class="fas fa-search"></i>
      <mu-text-field v-if='auth' color='indigo50' v-model="form.textarea" class = 'search-field' v-on:keyup.enter='submitSearch'></mu-text-field> -->
      TwittBro

      <mu-button flat slot='right' v-if='!auth' @click='goLogin'>Вход</mu-button>
      <mu-button flat slot='right' v-else @click='logout'>Выход</mu-button>
    </mu-appbar>
    <mu-bottom-nav v-if='auth'>

      <mu-button flat color="primary" @click="goToNews">Новости</mu-button>
      <mu-button flat color="primary" @click="goToMyWall">Моя страница</mu-button>
      <mu-button flat color="primary" @click="goToFollows">Мои подписки</mu-button>
      <mu-button flat color="primary" @click="goToMessenger">Мои сообщения</mu-button>
      <mu-button flat color="primary" @click="">Поиск</mu-button>

    </mu-bottom-nav>
    <slot></slot>
  </mu-container>
</template>

<script>


  export default {
    name: 'Home',
    // data() {
    //   return {
    //     form: {
    //       textarea: '',
    //     },
    //   }
    // },
    computed: {
      auth(){
        if (sessionStorage.getItem('auth_token')){
          return true
        }
      }
    },
    methods:{
      goLogin(){
        this.$router.push({name: 'login'})
      },
      logout() {
        sessionStorage.removeItem('auth_token')
        window.location = '/'
      },
      // submitSearch(){
      //   if (this.form.textarea.length === 0 || !this.form.textarea.trim()) {
      //     alert('Введите что-нибудь')
      //   }
      //   else{
      //     this.$router.push({name: 'search', params: {text: this.form.textarea}})
      //   }
      // },
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
    /* position: fixed; */
  }
</style>
