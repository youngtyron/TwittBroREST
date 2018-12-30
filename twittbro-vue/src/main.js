// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import MuseUI from 'muse-ui';
import 'muse-ui/dist/muse-ui.css';
Vue.use(MuseUI);
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  data:{
    galleryUrls: '',
    currentUrl: '',
    openGallerySlot: false,
    unreadPinkMessages: '',
  },
  methods:{
    pinkMessagesFunc(){
      $.ajax({
         url: 'http://127.0.0.1:8000/api/messenger/unread/',
         type: "GET",
         success: (response) => {
             if (response.data.data != 0){
               this.$root.unreadPinkMessages =  String(response.data.data)
             }
             else {
               this.$root.unreadPinkMessages = ''
             }
           }
      })
    },
  },
  router,
  components: { App },
  template: '<App/>'
})
