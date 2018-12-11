<template>
  <div>
    <HomeSlot>
      <div class="user-info">
        <p class="user-name">{{user.first_name}} {{user.last_name}}</p>
        <img class='avatar' alt=''/>
        <div v-if='!mywall'>
            <p>
              <mu-button v-if='!you_follow' flat color="secondary" @click="followUser">Подписаться</mu-button>
              <mu-button v-else flat color="primary" @click="followUser">Отписаться</mu-button>
            </p>
            <p>
              <mu-button flat color="primary" @click="openWriterWindow">Отправить сообщение <i class="fas fa-pen-alt"></i></mu-button>
            </p>
            <mu-dialog width="600" max-width="80%" :esc-press-close="false" :overlay-close="false" :open.sync="openWriter">
                <mu-text-field  :rows="4" multi-line full-width v-model="form2.textarea2" placeholder="Напечатайте текст сообщения"></mu-text-field>
                <mu-button slot="actions" flat color="normal" @click="openAddToChat">Добавить пользователя в чат?</mu-button>
                <mu-button slot="actions" flat color="primary" @click="closeWriterWindow">Отмена</mu-button>
                <mu-button slot="actions" flat color="secondary" @click="writeMessage">Отправить</mu-button>
              </mu-dialog>
              <mu-dialog width="600" max-width="80%" :esc-press-close="false" :overlay-close="false" :open.sync="openChatsList">

                <p>Выберите чат</p>
                <select v-model="selectedChat" class="select-chat">
                    <option v-for="chat in chats" v-bind:value="chat.id">
                      <p v-for='member in chat.members'>{{member.first_name}} {{member.last_name}}</p>
                    </option>
                </select>

                  <mu-button slot="actions" flat color="primary" @click="closeChatsWindow">Отмена</mu-button>
                  <mu-button slot="actions" flat color="secondary" @click="addSelectedChat">Добавить</mu-button>

              </mu-dialog>

        </div>
      </div>
      <div v-if='mywall'>
        <mu-text-field v-model="form.textarea" placeholder="Отправьте новый пост"></mu-text-field>
        <mu-button round color="secondary" @click="newPost">Отправить</mu-button>
      </div>
      <div class='central-strip' v-for='post in posts' :value="post.id">
        <i @click='deletePost' v-if='mywall' class="fas fa-times fa-2x deleting-cross" v-on:mouseover = 'darkCross' v-on:mouseout = 'lightCross'></i>
        <p class='post-text'>{{post.text}}</p>
        <p>{{post.pub_date}}</p>
        <i v-if = 'post.red' class="fas fa-heart fa-2x liking-heart red-heart" @click='likePost'>{{post.likes_quanity}}</i>
        <i v-else class="far fa-heart fa-2x liking-heart" @click='likePost'>{{post.likes_quanity}}</i>
      </div>
    </HomeSlot>
  </div>
</template>

<script>

    import HomeSlot from '@/components/Home.vue'

    export default{
      name: 'Wall',
      props: {
          id: '',
      },
      components: {
        HomeSlot,
      },
      data() {
        return {
          posts: '',
          form: {
            textarea: '',
          },
          form2: {
            textarea2: '',
          },
          mywall: '',
          user: '',
          you_follow: '',
          openWriter: false,
          openChatsList: false,
          chats: '',
          selectedChat: '',
        }
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadUser();
           this.getAva();
           this.loadPosts();
           window.addEventListener('scroll', this.scrollToCounter);
      },
      methods: {
        addSelectedChat(){
          var chat = this.selectedChat
          $.ajax({
             url: 'http://127.0.0.1:8000/api/messenger/get_chats_to_add_user/' + this.$route.params.id + '/',
             type: "POST",
             data: {
                 chat: chat,
             },
             success: (response) => {
               this.openChatsList = false
               alert('Пользователь добавлен в чат')
             },
             error: (response)=> {
               alert('Ошибка. Повторите снова')
             }
          })
        },

        getChats(){
          $.ajax({
            url: 'http://127.0.0.1:8000/api/messenger/get_chats_to_add_user/' + this.$route.params.id + '/',
            type: 'GET',
            success: (response)=>{
              this.chats = response.data.data
            },
          })
        },
        writeMessage(){
          $.ajax({
            url: 'http://127.0.0.1:8000/api/messenger/write/' + this.$route.params.id + '/',
            type: 'POST',
            data: {
                text: this.form2.textarea2
            },
            success: (response)=>{
              this.form2.textarea2 = ''
              this.closeWriterWindow()
              alert('Сообщение отправлено')

            },
            error: (response)=>{
              if (response.responseJSON.errors.empty){
                alert('Введите текст в поле ввода')
              }
            },
          })
        },
        openAddToChat(){
          this.openWriter = false;
          this.openChatsList = true;
          this.getChats();
        },
        closeChatsWindow(){
          this.openChatsList = false;
        },
        openWriterWindow () {
          this.openWriter = true;
        },
        closeWriterWindow () {
          this.openWriter = false;
        },
        scrollToCounter(){
          if($(window).scrollTop() + $(window).height() == $(document).height()) {
            this.loadPosts()
          }
        },
        getAva(){
          $.ajax({
             url: 'http://127.0.0.1:8000/api/profiles/avatar/' + this.$route.params.id + '/',
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
        followUser(){
          $.ajax({
             url: 'http://127.0.0.1:8000/api/profiles/follow/' + this.$route.params.id + '/',
             type: "POST",
             success: (response) => {
               if (response.data.create_follow){
                 this.you_follow = true
                 alert('Теперь вы подписаны на этого пользователя')
               }
               else if (response.data.delete_follow){
                 this.you_follow = false
                 alert('Вы отписались от этого пользователя')

               }
             },
             error: (response)=> {
               alert('Ошибка. Повторите снова')
             },
          })
        },
        loadUser(){
          $.ajax({
             url: 'http://127.0.0.1:8000/api/profiles/user/' + this.$route.params.id + '/',
             type: "GET",
             success: (response) => {
                this.user =  response.data.data
                if (response.data.you_follow){
                  this.you_follow = true
                }
             }
          })
        },
        loadPosts() {
            if (this.posts.length == 0){
              var last = 0
            }
            else{
              var last = this.posts[this.posts.length - 1].id
            }

            $.ajax({
               url: 'http://127.0.0.1:8000/api/profiles/posts/' + this.$route.params.id + '/',
               type: "GET",
               data: {
                   last: last,
               },
               success: (response) => {
                   if (this.posts.length == 0){
                     this.posts =  response.data.data
                   }
                   else{
                     this.posts =  this.posts.concat(response.data.data)
                   }
                   if (response.data.mywall){
                     this.mywall = true;
                   }
               }
            })
          },
        newPost(){
          $.ajax({
            url: 'http://127.0.0.1:8000/api/profiles/posts/' + this.$route.params.id + '/',
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
              if (this.posts != ''){
                this.posts = this.posts.concat(response.data.data)
                this.posts.unshift(this.posts[this.posts.length - 1])
                this.posts.splice(- 1, 1)
              }
              else{
                this.posts = response.data.data
              }
              }
            },
          })
        },
        deletePost(event){
          var id = event.target.parentNode.getAttribute('value')
          $.ajax({
            url: 'http://127.0.0.1:8000/api/profiles/delete_post/' + this.$route.params.id + '/',
            type: 'POST',
            data: {
                id: id,
            },
            success: (response)=>{
              var index;
              for (index = 0; index < this.posts.length; ++index) {
                if (this.posts[index].id == id){
                  this.posts.splice(index, 1)
                }
              }
            },
            error: (response)=> {
              alert('Ошибка. Повторите снова')
            }
          })
        },
        likePost(event){
          $.ajax({
            url: 'http://127.0.0.1:8000/api/profiles/like_post/',
            type: 'POST',
            data: {
                id: event.target.parentNode.getAttribute('value')
            },
            success: (response)=>{
              if (response.data.red == true){
                event.target.classList.remove('far');
                event.target.classList.add('fas');
                event.target.classList.add('red-heart');
              }
              else if (response.data.white == true){
                event.target.classList.remove('fas');
                event.target.classList.add('far');
                event.target.classList.remove('red-heart');
              }
              event.target.innerHTML = response.data.likes
            },
            error: (response)=> {
              alert('Ошибка. Повторите снова')
            }
          })
        },
        darkCross(e){
          e.target.style.opacity='1';
        },
        lightCross(e){
          e.target.style.opacity='0.3';
        },
      },
    }
</script>

<style scoped>
  .deleting-cross{
    float: right;
    opacity: 0.3;
  }
  .liking-heart{
    float: left;
  }
  .red-heart{
    color: crimson;
  }
  .user-info{
    float: left;
  }
  .post-text{
    font-size: 150%;
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
  .chat-in-window{
    border: 1px solid #C1C1C1;
  }
  .select-chat{
    width: 100%;
    height: 30px;
  }
</style>
