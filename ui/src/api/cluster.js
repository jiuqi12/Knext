import request from '@/utils/request'

// 资源总览模块
export function getOverview() {
  return request({
    url: '/overview',
    method: 'get'
  })
}

// 创建资源
export function createResource(data) {
  return request({
    url: '/create_resource',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'text/plain'
    }
  })
}

// 节点模块
// 获取全部节点
export function getNodes() {
  return request({
    url: '/nodes',
    method: 'get'
  })
}

// 命名空间模块
// 获取全部命名空间
export function getNamespaces() {
  return request({
    url: '/namespaces',
    method: 'get'
  })
}
// 删除命名空间
export function deleteNamespace(namespace_name) {
  return request({
    url: `/namespaces/${namespace_name}`,
    method: 'delete'
  })
}

// 工作负载模块
// 容器组模块
// 获取全部Pod
export function getPods(namespace) {
  return request({
    url: '/workloads/pods',
    method: 'get',
    params: {
      namespace
    }
  })
}
// 删除Pod
export function deletePod(namespace, pod_name) {
  return request({
    url: `/workloads/pods/${namespace}/${pod_name}`,
    method: 'delete'
  })
}
// 获取终端
// 获取日志

// deployment模块
// 获取全部deployment
export function getDeployments(namespace) {
  return request({
    url: `/workloads/deployments`,
    method: 'get',
    params: {
      namespace
    }
  })
}
// 删除deployment
export function deleteDeployment(deployment_name, namespace) {
  return request({
    url: `/workloads/deployments/${deployment_name}/${namespace}`,
    method: 'delete'
  })
}
// 获取daemonset列表
export function getDaemonsets(namespace) {
  return request({
    url: `/workloads/daemonsets`,
    method: 'get',
    params: {
      namespace
    }
  })
}
// 删除daemonset
export function deleteDaemonset(namespace, daemonset_name) {
  return request({
    url: `/workloads/daemonsets/${namespace}/${daemonset_name}`,
    method: 'delete'
  })
}

// 获取statefulset列表
export function getStatefulsets(namespace) {
  return request({
    url: `/workloads/statefulsets`,
    method: 'get',
    params: {
      namespace
    }
  })
}

export function deleteStatefulset(namespace, statefulset_name) {
  return request({
    url: `/workloads/statefulsets/${namespace}/${statefulset_name}`,
    method: 'delete'
  })
}

// 获取job列表
export function getJobs(namespace) {
  return request({
    url: `/workloads/jobs/${namespace}`,
    method: 'get'
  })
}
// 删除job
export function deleteJob(namespace, job_name) {
  return request({
    url: `/workloads/jobs/${namespace}/${job_name}`,
    method: 'delete'
  })
}

// 存储模块
// pv模块
// 获取全部pv
export function getPvs(namespace) {
  return request({
    url: `/storages/pvs/${namespace}`,
    method: 'get'
  })
}
// 删除pv
export function deletePv(namespace, pv_name) {
  return request({
    url: `/storages/pvs/${namespace}/${pv_name}`,
    method: 'delete'
  })
}

// pvc模块
// 获取全部pvc
export function getPvcs() {
  return request({
    url: '/storages/pvcs',
    method: 'get'
  })
}
// 删除pvc
export function deletePvc(namespace, pvc_name) {
  return request({
    url: `/storages/pvcs/${namespace}/${pvc_name}`,
    method: 'delete'
  })
}

// storageclass模块
// 获取storageclass
export function getStorageClasses() {
  return request({
    url: '/storages/storageclasses',
    method: 'get'
  })
}
// 删除storageclass
export function deleteStorageClass(name) {
  return request({
    url: `/storages/storageclasses/${name}`,
    method: 'delete'
  })
}

// 安全模块
// sa模块
// 获取全部sa
export function getAllSas() {
  return request({
    url: '/securities/sas',
    method: 'get'
  })
}
// 获取sa
export function getSas(namespace) {
  return request({
    url: '/securities/sas',
    method: 'get',
    params: {
      namespace
    }
  })
}

// 删除sa
export function deleteSas(namespace, sa_name) {
  return request({
    url: `/securities/sas/${namespace}/${sa_name}`,
    method: 'delete'
  })
}

// 角色模块
// 获取全部roles
export function getRoles() {
  return request({
    url: '/securities/roles',
    method: 'get'
  })
}

// 删除角色
export function deleteRoles(namespace, role_name) {
  return request({
    url: `/securities/roles/${namespace}/${role_name}`,
    method: 'delete'
  })
}

// 集群角色模块
// 获取全部clusterrole
export function getClusterRoles() {
  return request({
    url: '/securities/clusterroles',
    method: 'get'
  })
}

// 删除clusterrole
export function deleteClusterRoles(name) {
  return request({
    url: `/securities/clusterroles/${name}`,
    method: 'delete'
  })
}

// 获取rolebinding
export function getRoleBinding() {
  return request({
    url: '/securities/rolebindings',
    method: 'get'
  })
}

// 删除rolebinding
export function deleteRoleBinding(namespace, rb_name) {
  return request({
    url: `/securities/rolebindings/${namespace}/${rb_name}}`,
    method: 'delete'
  })
}

// 获取clusterrolebinding
export function getClusterRoleBinding(namespace) {
  return request({
    url: `/securities/clusterrolebindings/${namespace}`,
    method: 'get'
  })
}

// 删除clusterrolebinding
export function deleteClusterRoleBinding(namespace, crb_name) {
  return request({
    url: `/securities/clusterrolebindings/${namespace}/${crb_name}`,
    method: 'delete'
  })
}

// 网络模块
export function getService(namespace) {
  return request({
    url: '/networks/services',
    method: 'get',
    params: {
      namespace
    }
  })
}

// 配置模块
// configmaps
export function getConfigmapsnamespace(namespace) {
  return request({
    url: `/configs/configmaps`,
    method: 'get',
    params: {
      namespace
    }
  })
}
// 删除configmap
export function deleteConfigmap(namespace, configmap_name) {
  return request({
    url: `/configs/configmaps/${namespace}/${configmap_name}`,
    method: 'delete'
  })
}

// secrets模块
// 获取全部的secrets
export function getSecrets(namespace) {
  return request({
    url: `configs/secrets`,
    method: 'get',
    params: {
      namespace
    }
  })
}
// 删除secret
export function deleteSecret(namespace, secret_name) {
  return request({
    url: `/configs/secrets/${namespace}/${secret_name}`,
    method: 'delete'
  })
}
