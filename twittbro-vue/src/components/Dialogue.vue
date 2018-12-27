<template>
  <div v-on:mousemove='prereadMessages'>
    <HomeSlot>

        <div class="user-info">
          <p class="user-name">{{user.first_name}} {{user.last_name}}</p>
          <img class='avatar' alt=''/>

        </div>

          <div class="chat-info">
            <p v-for='companion in chat.chat_name' :id = 'companion.id' @click='companionLink(companion.id)'>{{companion.first_name}} {{companion.last_name}}</p>
          </div>

          <div id="message-box" v-on:scroll='scrollBox'>


            <div class='central-strip' v-for='message in messages' :value='message.id'>

              <div class='one-message grey my_grey' v-if='message.my_grey' :id='message.id'>
                <p v-if='message.writer.id == user.id' class='message-author right-message' >{{message.writer.first_name}}</p>
                <p v-else class='message-author left-message' >{{message.writer.first_name}}</p>


                <p v-if='message.writer.id == user.id'class='message-text right-message'>{{message.text}}</p>
                <p v-else class='message-text left-message'>{{message.text}}</p>


                <p v-if='message.writer.id == user.id' class='message-date right-message'>{{message.pub_date}}</p>
                <p v-else class='message-date left-message'>{{message.pub_date}}</p>

              </div>
              <div class='one-message grey' v-else-if='message.grey' :id='message.id'>
                <p v-if='message.writer.id == user.id' class='message-author right-message' >{{message.writer.first_name}}</p>
                <p v-else class='message-author left-message' >{{message.writer.first_name}}</p>


                <p v-if='message.writer.id == user.id'class='message-text right-message'>{{message.text}}</p>
                <p v-else class='message-text left-message'>{{message.text}}</p>


                <p v-if='message.writer.id == user.id' class='message-date right-message'>{{message.pub_date}}</p>
                <p v-else class='message-date left-message'>{{message.pub_date}}</p>

              </div>

              <div class='one-message white' v-else :id='message.id'>
                <p v-if='message.writer.id == user.id' class='message-author right-message' >{{message.writer.first_name}}</p>
                <p v-else class='message-author left-message' >{{message.writer.first_name}}</p>


                <p v-if='message.writer.id == user.id'class='message-text right-message'>{{message.text}}</p>
                <p v-else class='message-text left-message'>{{message.text}}</p>


                <p v-if='message.writer.id == user.id' class='message-date right-message'>{{message.pub_date}}</p>
                <p v-else class='message-date left-message'>{{message.pub_date}}</p>

              </div>
            </div>


          </div>

          <div class='print-block'>
            <mu-text-field id='message-input' v-model="form.textarea" placeholder="Отправьте новое сообщение"></mu-text-field>
            <mu-button round color="secondary" @click="sendMessage">Отправить</mu-button>
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
          last: '',
          chat: '',
        }
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadMyUser();
           this.getAva();
           this.loadMessages();
           window.addEventListener('keypress', this.keyWriteListener);
           setInterval(() => {
             this.newMessages()
           }, 10000)

      },
      methods: {
        keyWriteListener(event){
          if (event.keyCode == 13){
            if (document.activeElement == document.getElementById('message-input')){
              this.sendMessage()
            }
          }
          else{
            return null
          }
        },
        companionLink(id){
          this.$router.push({name: 'wall', params: {id: id}})
        },
        newMessages(){
          var newest = this.messages[this.messages.length - 1].id
          $.ajax({
            url: 'http://127.0.0.1:8000/api/messenger/new/' + this.$route.params.id + '/',
            type: 'GET',
            data: {
              newest: newest,
            },
            success: (response)=>{
              if (response.data.not_new!=true){
                this.messages = this.messages.concat(response.data.data)
              }
            },
          })
        },
        prereadMessages(){
          var my_grey = $('.my_grey');
          if (my_grey.length > 0){
            this.readMessages()
          }
        },
        readMessages(){
          var grey = $('.my_grey');
          var ids = new Array()
          for (var i = 0; i < grey.length; i++){
            ids[i]=grey[i].parentNode.getAttribute('value')
          }
          $.ajax({
            url: 'http://127.0.0.1:8000/api/messenger/read/' + this.$route.params.id + '/',
            type: 'POST',
            data: {
              ids,
            },
            success: (response)=>{
              for (var i = 0; i < response.data.white.length; i++){
                var elem = document.getElementById(response.data.white[i])
                elem.classList.add("white")
                elem.classList.remove("my_grey")
                elem.classList.remove("grey")
              }
            },
          })
        },
        scrollBox(){
          if ($('#message-box').scrollTop()==0){
            this.loadMessages()
          }
        },
        loadMessages(){
          if (this.messages.length == 0){
            var last = 0
          }
          else{
            var last = this.messages[0].id
          }
          $.ajax({
             url: 'http://127.0.0.1:8000/api/messenger/chat/' + this.$route.params.id + '/',
             type: "GET",
             data: {
               last: last,
             },
             success: (response) => {
               if (this.messages.length == 0){
                 this.messages =  response.data.data
               }
               else {
                 this.messages =  response.data.data.concat(this.messages)
               }
               this.chat = response.data.chatdata
                 // var block = document.getElementById("message-box");
                 // block.scrollTop = block.scrollHeight
                 $('#message-box').scrollTop = $('#message-box').scrollHeight
               }
          })
        },
        scrollDown(){
          var block = document.getElementById("message-box");
          block.scrollTop = block.scrollHeight;
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
              if (response.data.empty){
                alert('Введите текст в поле ввода')
              }
              else{
                this.messages = this.messages.concat(response.data.data)
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
#message-box {
  height: 500px;
  width: 65%;
  background: #fff;
  border: 1px solid #C1C1C1;
  overflow-y: scroll;
  margin-top: 20px;
}
.print-block{
  margin-top: 10px;
}
.message-author{
  font-size: 120%;
}
.message-date{
  font-size: 80%;
  color: grey;
}
.left-message{
  text-align: left;
}
.right-message{
  text-align: right;
}
.grey{
  background-color:rgb(242, 248, 250);
}

</style>
