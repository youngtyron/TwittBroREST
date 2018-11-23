<template>
  <div>
    <HomeSlot>
      <div v-for='post in posts'>
        <p>{{post.author.first_name}} {{post.author.last_name}}</p>
        <p>{{post.text}}</p>
        <p>{{post.pub_date}}</p>
      </div>
      <mu-text-field v-model="form.textarea" placeholder="Отправьте новый пост"></mu-text-field>
      <mu-button round color="secondary" @click="newPost">Отправить</mu-button>
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
          }
        }
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadPosts()
       },
      methods: {
        loadPosts() {
            $.ajax({
               url: 'http://127.0.0.1:8000/api/profiles/posts/' + this.$route.params.id + '/',
               type: "GET",
               success: (response) => {
                   this.posts = response.data.data
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
              alert('SENT')
              this.form.textarea = ''
              this.loadPosts()
            },
            error: (response)=> {
              if (response.data == 'empty'){
                alert('Введите текст в поле ввода')
              }
            }
          })
        },
      },
    }
</script>

<style scoped>

</style>
