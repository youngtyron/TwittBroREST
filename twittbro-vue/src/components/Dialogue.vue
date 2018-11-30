<template>
  <div>
    <HomeSlot>
      <div class="user-info">
        <p class="user-name">{{user.first_name}} {{user.last_name}}</p>
        <img class='avatar' alt=''/>

      </div>
        <div>
          <mu-text-field  v-model="form.textarea" placeholder="Отправьте новое сообщение"></mu-text-field>
          <mu-button round color="secondary" @click="sendMessage">Отправить</mu-button>
        </div>
        <div class='central-strip' v-for='message in messages' >
            <p class='message-author' >{{message.writer.first_name}}</p>
            <p class='message-text'>{{message.text}}</p>
        </div>
    </HomeSlot>
  </div>
</template>

<script>

    import HomeSlot from '@/components/Home.vue'

    export default{
      name: 'Messenger',
      props: {
          id: '',
      },
      components: {
        HomeSlot,
      },
      data() {
        return {
          user: '',
          messages: '',
          form: {
            textarea: '',
          },
        }
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadMyUser();
           this.getAva();
           this.loadMessages();
      },
      methods: {
        loadMessages(){
          $.ajax({
             url: 'http://127.0.0.1:8000/api/messenger/chat/' + this.$route.params.id + '/',
             type: "GET",
             success: (response) => {
                 this.messages =  response.data.data
               }
          })
        },
        sendMessage(){
          $.ajax({
            url: 'http://127.0.0.1:8000/api/messenger/chat/' + this.$route.params.id + '/',
            type: 'POST',
            data: {
                text: this.form.textarea
            },
            success: (response)=>{
              this.form.textarea = ''
              console.log(response.data)
              if (response.data.empty){
                alert('Введите текст в поле ввода')
              }
              else{
                this.messages = this.messages.concat(response.data.data)
                this.messages.unshift(this.messages[this.messages.length - 1])
                this.messages.splice(- 1, 1)
              }
            },

          })
        },
        loadMyUser(){
          $.ajax({
             url: 'http://127.0.0.1:8000/api/profiles/user_news/',
             type: "GET",
             success: (response) => {
                this.user =  response.data.data

             }
          })
        },
        // userLink(id){
        //   this.$router.push({name: 'wall', params: {id: id}})
        // },
        getAva(){
          $.ajax({
             url: 'http://127.0.0.1:8000/api/profiles/avatarnews/',
             type: "GET",
             success: (response) => {
                 var ava_url = '/static' + response.data.data
                 $(".avatar").attr("src", ava_url);
             },
             error: (response)=> {
               $(".avatar").attr("src", '/static/static/images/avatar.jpeg');
             },
          })
        },
      },
    }
</script>

<style scoped>

  .user-info{
    float: left;
  }
  .user-name{
    font-size: 150%;
    color: #039be5;
  }
  .central-strip{
    width: 60%;
    margin: auto;
  }
  .avatar{
    width: 150px;
    height: 150px;
    border-radius: 100px;
  }


</style>
