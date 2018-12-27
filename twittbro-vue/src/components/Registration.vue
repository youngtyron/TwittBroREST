<template>
  <HomeSlot>
    <div class='register-block'>
      <!-- <input v-model='username' type='text' placeholder="Логин"/> -->
      <mu-text-field v-model="username" placeholder="Логин"></mu-text-field>
      </br>
      <!-- <input v-model='first_name' type='text' placeholder="Имя"/> -->
      <mu-text-field v-model="first_name" placeholder="Имя"></mu-text-field>
      </br>
      <!-- <input v-model='last_name' type='text' placeholder="Фамилия"/> -->
      <mu-text-field v-model="last_name" placeholder="Фамилия"></mu-text-field>
      </br>
      <!-- <input v-model='email' type='text' placeholder="Электронная почта"/> -->
      <mu-text-field v-model="email" type="email" placeholder="Электронная почта"></mu-text-field>
      </br>
      <!-- <input v-model='password' type='password' placeholder="Пароль"/> -->
      <mu-text-field v-model="password" type='password' placeholder="Пароль"></mu-text-field>
      </br>
      <!-- <input v-model='confirm_password' type='password' placeholder="Подтверждение пароля"/> -->
      <mu-text-field v-model="confirm_password" type='password' placeholder="Подтверждение пароля"></mu-text-field>
      </br>
      <mu-button color="primary" @click="registrateUser">Отправить</mu-button>
      <!-- <button @click='registrateUser'>Отправить</button> -->
      </br>
      <p class='blue-link' @click='goLogin'>Уже зарегистрированы?</p>
    </div>
  </HomeSlot>
</template>

<script>

import HomeSlot from '@/components/Home.vue'


    export default{
      name: 'Registration',
      components: {
        HomeSlot,
      },
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
              this.$router.push({name: 'login'})
            },
            error:(response)=>{
              if (response.status === 400){
                console.log('400')
                if (response.data == 'pass_error'){
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
    font-size: 120%;
    color: #039be5;
  }
  .register-block{
    margin-top: 25px;
  }
</style>
