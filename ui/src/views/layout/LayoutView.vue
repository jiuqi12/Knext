<template>
  <el-container class="layout">
    <!-- 侧边栏 -->
    <el-aside class="sidebar" :width="isCollpase ? '64px' : '240px'">
      <el-scrollbar class="scrollbar">
        <el-menu
          class="menu"
          :collapse="isCollpase"
          :default-active="route.path"
          router
        >
          <!-- Logo -->
          <div class="logo">
            <h3>Knext 可视化面板</h3>
          </div>
          <!-- 总览 -->
          <el-menu-item index="/overview">
            <el-icon><Menu /></el-icon>
            <span>概览</span>
          </el-menu-item>
          <!-- 节点详情 -->
          <el-menu-item index="/nodes">
            <el-icon><location /></el-icon>
            <span>节点详情</span>
          </el-menu-item>
          <!-- 命名空间 -->
          <el-menu-item index="/namespaces">
            <el-icon><location /></el-icon>
            <span>命名空间</span>
          </el-menu-item>
          <el-menu-item index="/pods">
            <el-icon><location /></el-icon>
            <span>Pod容器组</span>
          </el-menu-item>
          <!-- 负载 -->
          <el-sub-menu index="/workloads">
            <template #title>
              <el-icon><location /></el-icon>
              <span>工作负载</span>
            </template>
            <el-menu-item index="/workloads/deployment">
              <el-icon><location /></el-icon>
              <span>Deployment</span>
            </el-menu-item>
            <el-menu-item index="/workloads/statefulset">
              <el-icon><location /></el-icon>
              <span>StatefulSet</span>
            </el-menu-item>
            <el-menu-item index="/workloads/daemonset">
              <el-icon><location /></el-icon>
              <span>DaemonSet</span>
            </el-menu-item>
            <el-menu-item index="/workloads/job">
              <el-icon><location /></el-icon>
              <span>Job</span>
            </el-menu-item>
          </el-sub-menu>
          <!-- 网络 -->
          <el-sub-menu index="network">
            <template #title>
              <el-icon><location /></el-icon>
              <span>网络</span>
            </template>
            <el-menu-item-group>
              <el-menu-item index="/networks/ingress">
                <el-icon><location /></el-icon>
                <span>Ingress</span>
              </el-menu-item>
              <el-menu-item index="/networks/service">
                <el-icon><location /></el-icon>
                <span>Service</span>
              </el-menu-item>
              <el-menu-item index="/networks/gateway">
                <el-icon><location /></el-icon>
                <span>Gateway</span>
              </el-menu-item>
            </el-menu-item-group>
          </el-sub-menu>
          <!-- 存储 -->
          <el-sub-menu index="storage">
            <template #title>
              <el-icon><location /></el-icon>
              <span>存储</span>
            </template>
            <el-menu-item index="/storages/pv">
              <el-icon><location /></el-icon>
              <span>PersistentVolume</span>
            </el-menu-item>
            <el-menu-item index="/storages/pvc">
              <el-icon><location /></el-icon>
              <span>PersistentVolumeClaim</span>
            </el-menu-item>
            <el-menu-item index="/storages/storageclass">
              <el-icon><location /></el-icon>
              <span>StorageClass</span>
            </el-menu-item>
          </el-sub-menu>
          <!-- 配置 -->
          <el-sub-menu index="configuration">
            <template #title>
              <el-icon><location /></el-icon>
              <span>配置</span>
            </template>
            <el-menu-item index="/configs/configmap">
              <el-icon><location /></el-icon>
              <span>ConfigMap</span>
            </el-menu-item>
            <el-menu-item index="/configs/secret">
              <el-icon><location /></el-icon>
              <span>Secret</span>
            </el-menu-item>
          </el-sub-menu>
          <!-- 安全 -->
          <el-sub-menu index="security">
            <template #title>
              <el-icon><location /></el-icon>
              <span>安全</span>
            </template>
            <el-menu-item index="/securities/sa">
              <el-icon><location /></el-icon>
              <span>ServiceAccount</span>
            </el-menu-item>
            <el-menu-item index="/securities/role">
              <el-icon><location /></el-icon>
              <span>Role</span>
            </el-menu-item>
            <el-menu-item index="/securities/rolebinding">
              <el-icon><location /></el-icon>
              <span>RoleBinding</span>
            </el-menu-item>
            <el-menu-item index="/securities/clusterrole">
              <el-icon><location /></el-icon>
              <span>ClusterRole</span>
            </el-menu-item>
            <el-menu-item index="/securities/clusterrolebinding">
              <el-icon><location /></el-icon>
              <span>ClusterRoleBinding</span>
            </el-menu-item>
          </el-sub-menu>
          <!-- 用户信息 -->
          <el-sub-menu v-if="isAdmin" index="/userrole">
            <template #title>
              <el-icon><location /></el-icon>
              <span>用户管理</span>
            </template>
            <el-menu-item index="/usermanagement">
              <el-icon><location /></el-icon>
              <span>用户管理</span>
            </el-menu-item>
            <el-menu-item index="/userroles">
              <el-icon><location /></el-icon>
              <span>用户角色管理</span>
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item v-else :index="`/userdetail/${userId}`">
            <el-icon><location /></el-icon>
            <span>个人中心</span>
          </el-menu-item>
        </el-menu>
      </el-scrollbar>
    </el-aside>
    <!-- 主内容区 -->
    <el-container class="main-container">
      <el-header class="header" height="60px">
        <div class="left">
          <!-- 折叠按钮 -->
          <el-icon
            :size="20"
            style="vertical-align: middle"
            @click="isCollpase = !isCollpase"
          >
            <Fold v-if="isCollpase" />
            <Expand v-else />
          </el-icon>
          <span class="split">|</span>
          <!-- 面包屑导航 -->
          <p class="breadcrumb">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item
                v-for="(value, index) in breadcrumbList"
                :key="index"
                >{{ value }}</el-breadcrumb-item
              >
            </el-breadcrumb>
          </p>
        </div>
        <div class="right">
          <el-icon :size="20"><Sunny /></el-icon>
          <el-dropdown>
            <span class="el-dropdown-link">
              <el-avatar
                :size="30"
                src="https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
              ></el-avatar>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item>个人资料</el-dropdown-item>
                <el-dropdown-item>设置</el-dropdown-item>
                <el-dropdown-item>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
defineOptions({
  name: 'LayoutView'
})
// 侧边栏折叠状态
import { ref, computed } from 'vue'
const isCollpase = ref(false)
const route = useRoute()
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
const isAdmin = userStore.isAdmin
const userId = userStore.userInfo?.uuid
console.log('isAdmin', isAdmin)
console.log('userId', userId)
// const router = useRouter()
// import { ElMessage } from 'element-plus'

// 面包屑导航
const breadcrumbList = computed(() => {
  return route.path.split('/').filter((p) => p)
})

// const handleCommand = (command) => {
//   console.log(command)
//   switch (command) {
//     case 'userinfo':
//       console.log('userinfo')
//       router.push('/userdetail/1')
//       break
//     case 'setting':
//       console.log('setting')
//       router.push('/userdetail/1')
//       break
//     case 'logout':
//       console.log('logout')
//       userStore.logout()
//       ElMessage.success('退出登录成功')
//       router.push('/login')
//       break
//   }
// }
</script>

<style lang="scss" scoped>
.layout {
  display: flex;
  height: 100vh;
  background-color: #f3f4f6;
  .sidebar {
    transition: width 0.3s ease;
    display: flex;
    flex-direction: column;
    margin: 5px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    &.el-menu--collapse {
      width: 64px;
    }
    .scrollbar {
      height: 100%;
      :deep(.el-scrollbar__bar) {
        opacity: 0;
      }
      .menu {
        flex: 1;
        border-right: none;
        color: #343a40;
        .logo {
          width: 100%;
          height: 60px;
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: center;
          border-bottom: 1px solid #e9ecef;
          h3 {
            text-align: center;
            line-height: 60px;
            color: #495057;
            font-size: 16px;
            font-weight: 600;
            margin: 0;
          }
        }
        .el-menu-item,
        .el-sub-menu__title {
          &:hover {
            background-color: #f3f4f6 !important;
          }
          &.is-active {
            background-color: #f3f4f6 !important;
            color: #5c7cfa !important;
          }
        }
      }
    }
  }
  .main-container {
    flex: 1;
    margin: 5px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    .header {
      height: 60px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 20px;
      border-bottom: 1px solid #e9ecef;
      .left {
        display: flex;
        align-items: center;
        gap: 15px;
        .el-icon {
          cursor: pointer;
          color: #495057;
          transition: color 0.3s ease;
          &:hover {
            color: #5c7cfa;
          }
        }
        .split {
          margin: 0 10px;
          color: #dee2e6;
        }
        .breadcrumb {
          margin: 0;
          .el-breadcrumb {
            opacity: 0.8;
            font-size: 14px;
            .el-breadcrumb-item {
              a {
                color: #495057;
                &:hover {
                  color: #5c7cfa;
                }
              }
            }
          }
        }
      }
      .right {
        display: flex;
        align-items: center;
        gap: 20px;
        .el-icon {
          cursor: pointer;
          color: #495057;
          transition: color 0.3s ease;
          &:hover {
            color: #5c7cfa;
          }
        }
        .el-dropdown-link {
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 10px;

          .el-avatar {
            border: 2px solid #e9ecef;
            transition: border-color 0.3s ease;
            &:hover {
              border-color: #5c7cfa;
            }
          }
        }
      }
    }
    .main {
      padding: 20px;
    }
  }
}
</style>
