<template>
  <div>
    <HomeSlot>
        <div class="user-info">
          <p class="user-name">{{user.first_name}} {{user.last_name}}</p>
          <img class='avatar' alt=''/>
        </div>

          <div class='central-strip' v-for='chat in chats' >
            <div :id="chat.id" class="dialogue" @click='oneDialog(chat.id)'>
              <p v-for='companion in chat.chat_name'>
                {{companion.first_name}} {{companion.last_name}}
                <mu-badge v-if='chat.new'   v-bind:content='String(chat.new)' circle color="secondary"  class="demo-icon-badge"></mu-badge>
              </p>
            </div>
          </div>
          <mu-button style='margin-top:10px;'round color="secondary" @click='openNewChatWindow'>Создать чат</mu-button>

          <mu-dialog width="600" max-width="80%" :esc-press-close="false" :overlay-close="false" :open.sync="openNewChat">
            <p>Выберите пользователей</p>
            <select multiple="true" v-model="selectedUser" class="select-user">
                <option v-for="p in people" v-bind:value="p.id">
                  {{p.first_name}} {{p.last_name}}
                </option>
            </select>
              <mu-button slot="actions" flat color="primary" @click="closeNewChatWindow">Отмена</mu-button>
              <mu-button slot="actions" flat color="secondary" @click="createChat">Создать чат</mu-button>
            </mu-dialog>

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
          openNewChat: false,
          people: '',
          selectedUser: [],
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
        createChat(){
          var users = this.selectedUser
          $.ajax({
             url: this.$root.baseUrl +'api/messenger/createchat/',
             data: {
               users: users,
             },
             type: "POST",
             success: (response) => {
                alert('Чат создан')
                this.openNewChat = false
              },
             error: (response) => {
               alert('Ошибка. Повторите снова')
             },
          })
        },
        openNewChatWindow(){
          this.openNewChat = true;
          this.getPeople();
        },
        getPeople(){
          $.ajax({
             url: this.$root.baseUrl +'api/messenger/createchat/',
             type: "GET",
             success: (response) => {
                 this.people =  response.data.data
               }
          })
        },
        closeNewChatWindow(){
          this.openNewChat = false;
        },
        loadChats(){
          $.ajax({
             url: this.$root.baseUrl +'api/messenger/chats/',
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
             url: this.$root.baseUrl +'api/profiles/user_news/',
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
