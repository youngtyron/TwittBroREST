<template>
  <div>
    <HomeSlot>
      <div v-if='mywall'>
        <mu-text-field  v-model="form.textarea" placeholder="Отправьте новый пост"></mu-text-field>
        <mu-button round color="secondary" @click="newPost">Отправить</mu-button>
      </div>
      <div v-for='post in posts' :value="post.id">
        <i @click='deletePost' v-if='mywall' class="fas fa-times fa-2x deleting-cross" v-on:mouseover = 'darkCross' v-on:mouseout = 'lightCross'></i>
        <p>{{post.author.first_name}} {{post.author.last_name}}</p>
        <p>{{post.text}}</p>
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
      components: {
        HomeSlot,
      },
      data() {
        return {
          posts: '',
          form: {
            textarea: '',
          },
          mywall: '',
          lastOnPage: 0,
        }
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadPosts()
           window.addEventListener('scroll', this.scrollToCounter);
      },
      methods: {
        scrollToCounter(){
          if($(window).scrollTop() + $(window).height() == $(document).height()) {
            this.loadPosts()
          }
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
              if (this.posts != ''){
                this.posts = this.posts.concat(response.data.data)
                this.posts.unshift(this.posts[this.posts.length - 1])
                this.posts.splice(- 1, 1)
              }
              else{
                this.posts = response.data.data
              }
            },
            error: (response)=> {
              if (response.data == 'empty'){
                alert('Введите текст в поле ввода')
              }
            }
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
</style>
