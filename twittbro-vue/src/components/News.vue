<template>
  <div>
    <HomeSlot>
      <div class="user-info">
        <p class="user-name">{{user.first_name}} {{user.last_name}}</p>
        <img class='avatar' alt=''/>
      </div>
      <div class='central-strip' v-for='post in posts' :value="post.id" :name='post.id'>
        <img :src='post.small_ava' class='small-avatar' alt=''/>
        <p @click='userLink(post.author.id)' class='post-author'>{{post.author.first_name}} {{post.author.last_name}}</p>

        <p class='post-text'>{{post.text}}</p>
        <div v-if='post.images_data'>
          <img class = 'one-image' v-for = 'image in post.images_data' :name='image.big' :src="image.small" alt="image" @click='showInGallery(image.big)'>
        </div>

        <div v-if='post.is_repost' class="repost-block">
          <div v-if='post.repost'>
            <img :src='post.repost.origin_ultra_ava' class='ultra-avatar' alt=''/>
            {{post.repost.origin_first_name}} {{post.repost.origin_last_name}}
            <p class='post-text'>{{post.repost.text}}</p>
            <div v-if='post.repost.images_data'>
              <img class = 'one-image' v-for = 'image in post.repost.images_data' :name='image.big' :src="image.small" alt="image" @click='showInGallery(image.big)'>
            </div>
            <p>{{post.repost.pub_date}}</p>
          </div>
          <div v-else>
            <p>Пост был удален</p>
          </div>
        </div>
        <p>{{post.pub_date}}</p>

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
      name: 'News',
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
          user: '',
          ImageCommentAddWindow: false,
          hooked_CommentFormData: '',
          post_for_imagecomment: '',

        }
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadMyUser();
           this.getAva();
           this.loadNews();
           window.addEventListener('scroll', this.scrollToCounter);
      },
      methods: {
        repost(id){
          $.ajax({
             url: this.$root.baseUrl +'api/profiles/repost/',
             type: "POST",
             data: {
                 id: id,
             },
             success: (response) => {
               this.posts = this.posts.concat(response.data.data)
               this.posts.unshift(this.posts[this.posts.length - 1])
               this.posts.splice(- 1, 1)
               this.posts[0]['commentform'] = {'textarea': ''}
               alert('Пост процитирован на вашей странице')

             },
             error: (response)=> {
               alert('Ошибка. Повторите снова')
             }
          })
        },
        userLink(id){
          this.$router.push({name: 'wall', params: {id: id}})
        },
        openImageCommentAddWindow(id){
          this.ImageCommentAddWindow = true
          this.post_for_imagecomment = id
        },
        addComment(post){
          var text = post.commentform.textarea
          if  (this.hooked_CommentFormData && this.post_for_imagecomment == post.id){
            var s = this
            const data = this.hooked_CommentFormData
            data.append('text', text)
            data.append('post', post.id)
            axios.post(this.$root.baseUrl +'api/profiles/comments/', data, {
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
               url: this.$root.baseUrl +'api/profiles/comments/',
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
        changeCommentImageInput(){
          var input = document.getElementById('commentimages')
          if (input.files.length>10){
            input.value = "";
            alert('Вы не можете отправлять более 10 изображений за раз. Добавьте изображения заново.')
          }
        },
        closeImageCommentAddWindow(){
          this.ImageCommentAddWindow = false
        },
        hookCommentImages(){
          this.hooked_CommentFormData = new FormData(document.getElementById('uploadCommentForm'))
          this.ImageCommentAddWindow = false
        },
        loadComments(post){
          var parent = document.getElementsByName(post.id)
          var comblock = $(parent).find('.comments-block')
          comblock.css('display', 'block')
          $(parent).find('.show-comments').css('display', 'none')
          $(parent).find('.hide-comments').css('display', 'block')
          if  (!post.comments.length){
            $.ajax({
               url: this.$root.baseUrl +'api/profiles/comments/',
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
        hideComments(id){
          var parent = document.getElementsByName(id)
          var comblock = $(parent).find('.comments-block')
          comblock.css('display', 'none')
          $(parent).find('.show-comments').css('display', 'block')
          $(parent).find('.hide-comments').css('display', 'none')
          post['comblock_isopen'] = false
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
        scrollToCounter(){
          if($(window).scrollTop() + $(window).height() == $(document).height()) {
            this.loadNews()
          }
        },
        loadNews(){
          if (this.posts.length == 0){
            var last = 0
          }
          else{
            var last = this.posts[this.posts.length - 1].id
          }
          $.ajax({
             url: this.$root.baseUrl +'api/profiles/news/',
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
             }
          })
        },

        loadMyUser(){
          $.ajax({
             url: this.$root.baseUrl +'api/profiles/user_news/',
             type: "GET",
             success: (response) => {
                this.user =  response.data.data
             }
          })
        },
        getAva(){
          $.ajax({
             url: this.$root.baseUrl +'api/profiles/avatarnews/',
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
        likePost(event){
          $.ajax({
            url: this.$root.baseUrl +'api/profiles/like_post/',
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
    /* border: 1px solid #C1C1C1; */

    width: 60%;
    margin: auto;
  }
  .avatar{
    width: 150px;
    height: 150px;
    border-radius: 100px;
  }
  .post-author{
    font-size: 150%;
    color: #039be5;
  }
  .small-avatar{
    width: 50px;
    height: 50px;
    border-radius: 50px;
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
