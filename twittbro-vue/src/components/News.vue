<template>
  <div>
    <HomeSlot>
      <div class="user-info">
        <p class="user-name">{{user.first_name}} {{user.last_name}}</p>
        <img class='avatar' alt=''/>
      </div>
      <div class='central-strip' v-for='post in posts' :value="post.id">
        <p class='post-author'>{{post.author.first_name}} {{post.author.last_name}}</p>
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
      name: 'News',
      components: {
        HomeSlot,
      },
      data() {
        return {
          posts: '',
          form: {
            textarea: '',
          },
          user: '',
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
             url: 'http://127.0.0.1:8000/api/profiles/news/',
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
               }             }
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
  .post-author{
    font-size: 150%;
    color: #039be5;
  }
</style>
