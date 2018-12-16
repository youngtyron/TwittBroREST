<template>
  <HomeSlot>
    <div>
      <input v-model='login' type='text' placeholder="Логин"/>
      <input v-model='password' type='password' placeholder="Пароль"/>
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
        }
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
      },
    }
</script>

<style scoped>
  .blue-link{
    font-size: 120%;
    color: #039be5;
  }
</style>
