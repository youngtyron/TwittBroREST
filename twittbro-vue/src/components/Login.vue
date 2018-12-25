<template>
  <HomeSlot>
    <div>
      <mu-text-field v-model="login" placeholder="Логин"></mu-text-field></br>
      <mu-text-field v-model="password" type='password' placeholder="Пароль"></mu-text-field></br>
      <button @click='setLogin'>Войти</button>
      <p class='blue-link' @click='goRegistrate'>Зарегистрироваться</p>
    </div>
  </HomeSlot>
</template>

<script>

    import HomeSlot from '@/components/Home.vue'

    export default{
      name: 'Login',
      components: {
        HomeSlot,
      },
      data() {
        return {
          login: '',
          password: '',
          visibility: false,
        }
      },
      created(){
        window.addEventListener('keypress', this.keyEnterListener);
      },
      methods: {
        setLogin(){
          $.ajax({
            url: 'http://127.0.0.1:8000/auth/token/create/',
            type:'POST',
            data: {
              username: this.login,
              password: this.password
            },
            success: (response)=>{
              sessionStorage.setItem('auth_token', response.data.attributes.auth_token)
              this.$router.push({name: 'mywall'})
            },
            error:(response)=>{
              if (response.status === 400){
                alert("Логин или пароль не верен")
              }
            }
          })
        },
        goRegistrate() {
          this.$router.push({name: "registration"})
        },
        keyEnterListener(event){
          if (event.keyCode == 13){
            if (this.login && this.password){
              this.setLogin()
            }
          }
          else{
            return null
          }
        },
      },
    }
</script>

<style scoped>
  .blue-link{
    font-size: 120%;
    color: #039be5;
  }
</style>
