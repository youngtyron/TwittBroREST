<template>
  <div>
    <HomeSlot>
              <div class="user-info">
                  <p class="user-name">{{user.first_name}} {{user.last_name}}</p>
                  <img class='avatar' alt=''/>
                  <p>
                    <mu-button v-if='mywall' color="secondary" @click="openAvatarWindow"><i class="fas fa-camera-retro"></i></mu-button>

                  </p>

                  <mu-dialog v-if='mywall' width="600" max-width="80%" :esc-press-close="false" :overlay-close="false" :open.sync="openAddAvatar">
                      <p style = 'font-size:120%;'>Смените фотографию профиля</p>

                    <form id="uploadForm" name="uploadForm" enctype="multipart/form-data">

                       <input type="file" id="files" name="files"><br>

                    </form>


                      <mu-button slot="actions" flat color="primary" @click="closeAvatarWindow">Отмена</mu-button>
                      <mu-button slot="actions" flat color="secondary" @click="this.uploadFiles">Отправить</mu-button>
                  </mu-dialog>
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
                  <i class="fas fa-camera fa-2x" @click="openImagePostAddWindow"></i>
                  <mu-button round color="secondary" @click="newPost">Отправить</mu-button>
                  <p class='text-hooked-images' v-if='this.count_hooked'>{{this.count_hooked}}</p>
                </div>

                <mu-dialog v-if='mywall' width="600" max-width="80%" :esc-press-close="false" :overlay-close="false" :open.sync="ImagePostAddWindow">
                    <p style = 'font-size:120%;'>Добавьте изображения к вашему посту</p>
                    <span>Вы можете прикрепить до 10 изображений</span><br>

                  <form id="uploadPostForm" name="uploadForm" enctype="multipart/form-data">

                     <input type="file" id="postimages" name="postimages" multiple v-on:change='changeImageInput'><br>

                  </form>

                    <mu-button slot="actions" flat color="primary" @click="closeImagePostAddWindow">Отмена</mu-button>
                    <mu-button slot="actions" flat color="secondary" @click="hookImages">Прикрепить</mu-button>
                </mu-dialog>

                <div class='central-strip' v-for='post in posts' :value="post.id" :name='post.id'>

                  <p v-if='post.repost'>
                    <img :src='post.repost.origin_ultra_ava' class='ultra-avatar' alt=''/>
                    {{post.repost.origin_first_name}} {{post.repost.origin_last_name}}
                  </p>

                  <i @click='deletePost' v-if='mywall' class="fas fa-times fa-2x deleting-cross" v-on:mouseover = 'darkCross' v-on:mouseout = 'lightCross'></i>
                  <p v-if='!post.repost' class='post-text'>{{post.text}}</p>
                  <p v-else class='post-text'>{{post.repost.text}}</p>
                  <p v-if='post.repost'>{{post.repost.pub_date}}</p>
                  <p>{{post.pub_date}}</p>
                  <div v-if='post.images_data'>
                    <img class = 'one-image' v-for = 'image in post.images_data' :name='image.big' :src="image.small" alt="image" @click='showInGallery(image.big)'>
                  </div>
                  <div v-if='post.repost'>
                    <div v-if='post.repost.images_data'>
                      <img class = 'one-image' v-for = 'image in post.repost.images_data' :name='image.big' :src="image.small" alt="image" @click='showInGallery(image.big)'>
                    </div>
                  </div>
                  <p v-if='post.comments' class="blue-link show-comments" @click='loadComments(post)'>Показать комментарии</p>
                  <p v-if='post.comments' class="blue-link hide-comments" @click='hideComments(post.id)'>Скрыть комментарии</p>
                  <div class="comments-block">
                    <div class="one-comment" v-for='comment in post.comments'>
                      <img :src='comment.ultra_avatar' class='ultra-avatar' alt=''/>
                      <p>{{comment.commentator.first_name}} {{comment.commentator.last_name}}</p>
                      <p>{{comment.text}}</p>
                      <div v-if='comment.images_data'>
                        <img class = 'one-image' v-for = 'image in comment.images_data' :name='image.big' :src="image.small" alt="image" @click='showInGallery(image.big)'>
                      </div>
                    </div>
                  </div>
                  <p>
                    <mu-text-field  :rows="2" multi-line width='50%' v-model="post.commentform.textarea" placeholder="Напечатайте свой комментарий"></mu-text-field>
                    <i class="fas fa-camera fa-2x" @click="openImageCommentAddWindow(post.id)"></i>
                    <i class="fas fa-chevron-right fa-2x" @click='addComment(post)'></i>
                  </p>


                    <i v-if = 'post.red' class="fas fa-heart fa-2x liking-heart red-heart" @click='likePost'>{{post.likes_quanity}}</i>
                    <i v-else class="far fa-heart fa-2x liking-heart" @click='likePost'>{{post.likes_quanity}}</i>
                    <i v-if='post.can_repost' @click='repost(post.id)' class="fas fa-share fa-2x"></i>

          </div>

          <mu-dialog width="600" max-width="80%" :esc-press-close="false" :overlay-close="false" :open.sync="ImageCommentAddWindow">
              <p style = 'font-size:120%;'>Добавьте изображения к вашему комментарию</p>
              <span>Вы можете прикрепить до 10 изображений</span><br>

            <form id="uploadCommentForm" name="uploadCommentForm" enctype="multipart/form-data">

               <input type="file" id="commentimages" name="commentimages" multiple v-on:change='changeCommentImageInput'><br>

            </form>

              <mu-button slot="actions" flat color="primary" @click="closeImageCommentAddWindow">Отмена</mu-button>
              <mu-button slot="actions" flat color="secondary" @click="hookCommentImages">Прикрепить</mu-button>
          </mu-dialog>

          <GallerySlot v-if='this.$root.openGallerySlot'></GallerySlot>

    </HomeSlot>
  </div>
</template>

<script>

    import HomeSlot from '@/components/Home.vue'
    import GallerySlot from '@/components/Gallery.vue'

    import axios from 'axios'

    export default{
      name: 'Wall',
      props: {
          id: '',
      },
      components: {
        HomeSlot,
        GallerySlot,
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
          openAddAvatar: false,
          ImagePostAddWindow: false,
          ImageCommentAddWindow: false,
          chats: '',
          selectedChat: '',
          image: '',
          hooked_FormData: '',
          hooked_CommentFormData: '',
          count_hooked: '',
          post_for_imagecomment: '',
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
        repost(id){
          $.ajax({
             url: 'http://127.0.0.1:8000/api/profiles/repost/',
             type: "POST",
             data: {
                 id: id,
             },
             success: (response) => {
               console.log('success')

             },
             error: (response)=> {
               alert('Ошибка. Повторите снова')
             }
          })
        },
        openImageCommentAddWindow(id){
          this.ImageCommentAddWindow = true
          this.post_for_imagecomment = id
        },
        hookCommentImages(){
          this.hooked_CommentFormData = new FormData(document.getElementById('uploadCommentForm'))
          this.ImageCommentAddWindow = false
        },
        closeImageCommentAddWindow(){
          this.ImageCommentAddWindow = false
        },
        changeCommentImageInput(){
          var input = document.getElementById('commentimages')
          if (input.files.length>10){
            input.value = ""
            alert('Вы не можете отправлять более 10 изображений за раз. Добавьте изображения заново.')
          }
        },
        addComment(post){
          var text = post.commentform.textarea
          if  (this.hooked_CommentFormData && this.post_for_imagecomment == post.id){
            var s = this
            const data = this.hooked_CommentFormData
            data.append('text', text)
            data.append('post', post.id)
            axios.post('http://127.0.0.1:8000/api/profiles/comments/', data, {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': "Token " + sessionStorage.getItem('auth_token')
              }
            })
              .then(response => {
                post.commentform.textarea = ''
                if (post.comments){
                  if (post.comblock_isopen){
                    post.comments = post.comments.concat(response.data.data.data)
                  }
                  else{
                    this.loadComments(post)
                  }
                  var parent = document.getElementsByName(post.id)
                  var comblock = $(parent).find('.comments-block')
                  comblock.css('display', 'block')
                  post['comblock_isopen'] = true
                  this.post_for_imagecomment = ''
                }
                else{
                  window.location.reload()
                }
              })
              .catch(error => {
                alert('Ошибка. Повторите снова')
              })
          }
          else{
            $.ajax({
               url: 'http://127.0.0.1:8000/api/profiles/comments/',
               type: "POST",
               data: {
                   post: post.id,
                   text: text,
               },
               success: (response) => {
                 post.commentform.textarea = ''
                 if (response.data.empty){
                   alert('Введите текст в поле ввода')
                 }
                 else{
                   if (post.comments){
                     if (post.comblock_isopen){
                       post.comments = post.comments.concat(response.data.data)
                     }
                     else{
                       this.loadComments(post)
                     }
                     var parent = document.getElementsByName(post.id)
                     var comblock = $(parent).find('.comments-block')
                     comblock.css('display', 'block')
                     post['comblock_isopen'] = true
                   }
                   else{
                     window.location.reload()
                   }
                 }
               },
               error: (response)=> {
                 alert('Ошибка. Повторите снова')
               }
            })
          }
        },
        hideComments(id){
          var parent = document.getElementsByName(id)
          var comblock = $(parent).find('.comments-block')
          comblock.css('display', 'none')
          $(parent).find('.show-comments').css('display', 'block')
          $(parent).find('.hide-comments').css('display', 'none')
          post['comblock_isopen'] = false
        },
        loadComments(post){
          var parent = document.getElementsByName(post.id)
          var comblock = $(parent).find('.comments-block')
          comblock.css('display', 'block')
          $(parent).find('.show-comments').css('display', 'none')
          $(parent).find('.hide-comments').css('display', 'block')
          if  (!post.comments.length){
            $.ajax({
               url: 'http://127.0.0.1:8000/api/profiles/comments/',
               type: "GET",
               data: {
                   post: post.id,
               },
               success: (response) => {
                 post['comments'] = response.data.data
                 post['comblock_isopen'] = true
               },
               error: (response)=> {
                 alert('Ошибка. Повторите снова')
               }
            })
          }
        },
        showInGallery(url){
          this.$root.currentUrl = url
          this.$root.galleryUrls = new Array()
          var curr = document.getElementsByName(url)[0]
          var bros = curr.parentNode.children;
          for (var i = 0; i < bros.length; ++i){
              this.$root.galleryUrls = this.$root.galleryUrls.concat(bros[i].getAttribute('name'))
          }
          this.$root.openGallerySlot = true
        },
        changeImageInput(){
          var input = document.getElementById('postimages')
          if (input.files.length>10){
            input.value = "";
            alert('Вы не можете отправлять более 10 изображений за раз. Добавьте изображения заново.')
          }
        },
        hookImages(){
          this.hooked_FormData = new FormData(document.getElementById('uploadPostForm'))
          this.ImagePostAddWindow = false
          var input = document.getElementById('postimages')
          console.log(input.files.length)
          if (input.files.length == 1){
            this.count_hooked = 'Прикреплено 1 изображение'
          }
          else if (input.files.length >1 && input.files.length < 5){
            this.count_hooked = 'Прикреплено ' + String(input.files.length) + ' изображения'
          }
          else {
            this.count_hooked = 'Прикреплено ' + String(input.files.length) + ' изображений'
          }
        },
        closeImagePostAddWindow(){
          this.ImagePostAddWindow = false
        },
        openImagePostAddWindow(){
          this.ImagePostAddWindow = true
        },
        uploadFiles () {
          var s = this
          const data = new FormData(document.getElementById('uploadForm'))
          var imagefile = document.querySelector('#files')
          data.append('file', imagefile.files[0])
          axios.post('http://127.0.0.1:8000/api/profiles/change_avatar/', data, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Authorization': "Token " + sessionStorage.getItem('auth_token')
            }
          })
            .then(response => {
              var ava_url = '/static' + String(response.data.data.data)
              $(".avatar").attr("src", ava_url);
              this.openAddAvatar = false;
            })
            .catch(error => {
              alert('Ошибка. Повторите снова')
            })
        },
        openAvatarWindow(){
          this.openAddAvatar = true;
        },
        closeAvatarWindow(){
          this.openAddAvatar = false;
        },
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
                   for (var i = 0; i<this.posts.length; ++i){
                     this.posts[i]['commentform'] = {'textarea': ''}
                   }
                   if (response.data.mywall){
                     this.mywall = true;
                   }
               }
            })
          },
        newPost(){
          if  (this.hooked_FormData){
            var s = this
            const data = this.hooked_FormData
            data.append('text', this.form.textarea)
            axios.post('http://127.0.0.1:8000/api/profiles/posts/' + this.$route.params.id + '/', data, {
              headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': "Token " + sessionStorage.getItem('auth_token')
              }
            })
              .then(response => {
                this.form.textarea = ''
                this.count_hooked = ''
                if (this.posts != ''){
                  this.posts = this.posts.concat(response.data.data.data)
                  this.posts.unshift(this.posts[this.posts.length - 1])
                  this.posts.splice(- 1, 1)
                }
                else{
                  this.posts = response.data.data.data
                }
                for (var i = 0; i<this.posts.length; ++i){
                  this.posts[i]['commentform'] = {'textarea': ''}
                }
              })
              .catch(error => {
                alert('Ошибка. Повторите снова')
              })
          }

          else {
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
                for (var i = 0; i<this.posts.length; ++i){
                  this.posts[i]['commentform'] = {'textarea': ''}
                }
                }
              },
            })
          }
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
  .one-image{
    margin-left: 3px;
    margin-right: 3px;
  }
  .blue-link{
    font-size: 120%;
    color: #039be5;
  }
  .comments-block{
    display: none;
  }
  .hide-comments{
    display: none;
  }
  .text-hooked-images{
    margin-right: 175px;
    margin-top: -10px;
    color: #039be5;
  }
  .ultra-avatar{
    width: 35px;
    height: 35px;
    border-radius: 35px;
  }
  .fa-share{
    float: left;
    margin-left: 10px;
  }
</style>
