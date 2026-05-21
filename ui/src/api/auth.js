import request from '@/utils/request'

// 登录模块
export function userLogin(data) {
  return request({
    url: '/users/login',
    method: 'post',
    data
  })
}

// 退出登录模块
export function userLogout() {
  return request({
    url: '/users/logout',
    method: 'post'
  })
}

// 列出用户模块
export function listUsers() {
  return request({
    url: '/users',
    method: 'get'
  })
}

// 创建或修改用户信息
export function createUser(data) {
  return request({
    url: '/users',
    method: 'post',
    data
  })
}

// 删除用户
export function deleteUser(user_id) {
  return request({
    url: `/users/${user_id}`,
    method: 'delete'
  })
}

// 修改用户状态
export function changeUser(user_id) {
  return request({
    url: `/users/${user_id}`,
    method: 'patch'
  })
}

// 获取用户详情
export function getUserDetail(username) {
  return request({
    url: `/users/${username}`,
    method: 'get'
  })
}

// 修改密码
export function changePassword(data) {
  return request({
    url: '/users/change-password',
    method: 'post',
    data
  })
}

// 列出用户角色
export function listUserRoles() {
  return request({
    url: '/users/userroles',
    method: 'get'
  })
}
