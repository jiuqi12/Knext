import { createApp } from 'vue'
import { createPinia } from 'pinia'
import persist from 'pinia-plugin-persistedstate'
import App from './App.vue'
import router from './router'
import 'element-plus/dist/index.css'
import '@/assets/base.css'
import '@/assets/iconfont.css'
import YamlEditor from '@/components/YamlEditor.vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

// 注册全局图标组件
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.component('YamlEditor', YamlEditor)

app.use(createPinia().use(persist))
app.use(router)

app.mount('#app')
