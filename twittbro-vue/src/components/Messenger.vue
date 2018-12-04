<template>
  <div>
    <HomeSlot>
        <div class="user-info">
          <p class="user-name">{{user.first_name}} {{user.last_name}}</p>
          <img class='avatar' alt=''/>

        </div>
          <div class='central-strip' v-for='chat in chats' >
            <div :id="chat.id" class="dialogue" @click='oneDialog(chat.id)'>
              <p>{{chat.name}}<mu-badge v-if='chat.new' v-bind:content='String(chat.new)' circle color="secondary"  class="demo-icon-badge"></mu-badge></p>
              <div v-for='member in chat.member'>
                {{member.username}}
              </div>

            </div>
          </div>
    </HomeSlot>
  </div>
</template>

<script>

    import HomeSlot from '@/components/Home.vue'

    export default{
      name: 'Messenger',
      components: {
        HomeSlot,
      },
      data() {
        return {
          user: '',
          chats: '',
        }
      },
      created() {
           $.ajaxSetup({
               headers: {'Authorization': "Token " + sessionStorage.getItem('auth_token')},
           });
           this.loadMyUser();
           this.getAva();
           this.loadChats();
      },
      methods: {
        loadChats(){
          $.ajax({
             url: 'http://127.0.0.1:8000/api/messenger/chats/',
             type: "GET",
             success: (response) => {
                 this.chats =  response.data.data
               }
          })
        },

        oneDialog(id){
          this.$router.push({name: 'dialogue', params: {id: id}})
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
  .dialogue{
    margin-top: 5px;
    border: solid black 1px;
  }

</style>
