import path from 'path'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Inspect from 'vite-plugin-inspect'
import { fileURLToPath } from 'url'

const pathSrc = fileURLToPath(new URL('./src', import.meta.url))
// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': pathSrc
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true
      },
      '/ws': {
        target: 'ws://127.0.0.1:8000',
        ws: true
      }
    }
  },
  plugins: [
    vue(),

    AutoImport({
      // 自动导入 vue 相关函数，如ref、reactive等
      imports: ['vue'],

      // 自动导入 Element Plus 相关函数，如ElMessage, ElMessageBox... (带样式)
      resolvers: [
        ElementPlusResolver(),

        // 自动导入图标组件
        IconsResolver({
          prefix: 'Icon'
        })
      ],
      dts: path.resolve(pathSrc, 'auto-imports.d.ts')
    }),

    Components({
      resolvers: [
        // 自动注册图标组件
        IconsResolver({
          enabledCollections: ['ep']
        }),

        // 自动注册element-plus组件
        ElementPlusResolver()
      ],

      dts: path.resolve(pathSrc, 'components.d.ts')
    }),

    Icons({
      autoInstall: true
    }),

    Inspect()
  ]
})
