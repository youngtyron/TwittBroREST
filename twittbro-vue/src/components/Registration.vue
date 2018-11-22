<template>
  <div>
    <input v-model='username' type='text' placeholder="Логин"/>
    <input v-model='first_name' type='text' placeholder="Имя"/>
    <input v-model='last_name' type='text' placeholder="Фамилия"/>
    <input v-model='email' type='text' placeholder="Электронная почта"/>
    <input v-model='password' type='password' placeholder="Пароль"/>
    <input v-model='confirm_password' type='password' placeholder="Подтверждение пароля"/>
    <button @click='registrateUser'>Отправить</button>
    <p class='blue-link' @click='goLogin'>Уже зарегистрированы?</p>
  </div>
</template>

<script>

    export default{
      name: 'Registration',
      data() {
        return {
          username: '',
          first_name: '',
          last_name: '',
          email: '',
          password: '',
          confirm_password: ''
        }
      },
      methods: {
        registrateUser(){
          $.ajax({
            url: 'http://127.0.0.1:8000/api/registate/',
            type:'POST',
            data: {
              username: this.username,
              first_name: this.first_name,
              last_name: this.last_name,
              email: this.email,
              password: this.password,
              confirm_password: this.confirm_password
            },
            success: (response)=>{
              alert("Вы успешно зарегистрированы!")
              this.$router.push({name: 'home'})
            },
            error:(response)=>{
              if (response.status === 400){
                if (response.data = 'pass_error'){
                  alert("Подтверждение пароля не совпадает")
                }
                else {
                  alert("Введите заново")
                }
              }
            }
          })
        },
        goLogin(){
          this.$router.push({name: 'login'})
        },
      },
    }
</script>

<style scoped>
  .blue-link{
    color: blue;
  }
</style>
