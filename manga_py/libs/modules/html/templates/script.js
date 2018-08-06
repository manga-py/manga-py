document.addEventListener('DOMContentLoaded', () => {
'use strict';

const Chapter = {
  template: `
<div class="slider-images">
      <router-view></router-view>
</div>
  `,
};

const router = new VueRouter({
    routes: [
        {
            path: '/ch/:id', component: Chapter,
            children: [
                {
                    // при совпадении пути с шаблоном /user/:id/profile
                    // в <router-view> компонента User будет показан UserProfile
                    path: 'profile',
                    component: UserProfile
                },
                {
                    // при совпадении пути с шаблоном /user/:id/posts
                    // в <router-view> компонента User будет показан UserPosts
                    path: 'posts',
                    component: UserPosts
                },
            ],
        },
    ],
});

new Vue({router}).$mount('#app');

});
