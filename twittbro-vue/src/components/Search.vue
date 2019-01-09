<template>
  <div>
    <HomeSlot>
      <div>
        <select v-model="selectedSearch" class="select-search">
            <option :value='1'>Поиск постов</option>
            <option :value='2'>Поиск пользователей</option>
        </select>
        <mu-text-field  :rows="2" v-model="form.textarea" placeholder="Введите текст для поиска"></mu-text-field>
        <mu-button color="primary" @click="searchFor"><i class="fas fa-search"></i></mu-button>
        {{question}}
        <div class='central-strip' v-for='post in posts' :value="post.id">
          <p class='post-author'>{{post.author.first_name}} {{post.author.last_name}}</p>
          <p class='post-text'>{{post.text}}</p>
          <p>{{post.pub_date}}</p>
          <i v-if = 'post.red' class="fas fa-heart fa-2x liking-heart red-heart" @click='likePost'>{{post.likes_quanity}}</i>
          <i v-else class="far fa-heart fa-2x liking-heart" @click='likePost'>{{post.likes_quanity}}</i>
        </div>
        <div class='central-strip' v-for='user in users' :value="user.id">
          <p class='user-string' @click='userLink(user.id)'>{{user.first_name}} {{user.last_name}}</p>
        </div>
      </div>
    </HomeSlot>
  </div>
</template>

<script>

    import HomeSlot from '@/components/Home.vue'

    export default{
      name: 'Search',
      data() {
        return {
          posts: '',
          users: '',
          form: {
            textarea: '',
          },
          selectedSearch: 1,
          question: '',
        }
      },
      components: {
        HomeSlot,
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           window.addEventListener('scroll', this.scrollToCounter);
       },
      methods: {
        userLink(id){
          this.$router.push({name: 'wall', params: {id: id}})
        },
        searchFor(){
          var type = this.selectedSearch
          var text = this.form.textarea
          this.question = this.form.textarea
          this.posts = ''
          this.users = ''
                $.ajax({
                   url: this.$root.baseUrl +'api/profiles/load_results/',
                   type: "GET",
                   data: {
                     text: text,
                     type: type,
                   },
                   success: (response) => {
                     if (type == '1'){
                       this.posts = response.data.data
                     }
                     else if (type == '2'){
                       this.users = response.data.data
                     }
                   },
                })
        },
        scrollToCounter(){
          if($(window).scrollTop() + $(window).height() == $(document).height()) {
            this.appendSearched()
          }
        },
        appendSearched(){
          if (this.posts){
            var last = this.posts[this.posts.length - 1].id
            var type = 'posts'
          }
          else if (this.users){
            var last = this.users[this.users.length - 1].id
            var type = 'users'
          }
          var question = this.question
          $.ajax({
             url: this.$root.baseUrl +'api/profiles/append_results/',
             type: "GET",
             data: {
               last: last,
               type: type,
               question: question,
             },
             success: (response) => {
               if (this.posts){
                 this.posts =  this.posts.concat(response.data.data)
               }
               else if (this.users){
                 this.users = this.users.concat(response.data.data)
               }
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
  .liking-heart{
    float: left;
  }
  .red-heart{
    color: crimson;
  }
  .post-text{
    font-size: 150%;
  }
  .post-author{
    font-size: 150%;
    color: #039be5;
  }
  .user-string{
    font-size: 150%;
    color: #039be5;
  }
  .central-strip{
    width: 60%;
    margin: auto;
  }
</style>
