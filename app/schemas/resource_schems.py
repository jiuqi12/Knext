# k8s 资源返回结构
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from datetime import datetime


class NamespaceListResponse(BaseModel):
    """命名空间列表响应"""
    namespaces: List[str]


class ClusterInfo(BaseModel):
    """集群信息"""
    totalNodes: int = Field(..., description="总节点数")
    readyNodes: int = Field(..., description="就绪节点数")
    totalNamespaces: int = Field(..., description="总命名空间数")
    totalServices: int = Field(..., description="总服务数")
    totalPods: int = Field(..., description="总 Pod 数")
    totalContainers: int = Field(..., description="总容器数")
    lastUpdated: str = Field(..., description="最后更新时间")


class ResourceUsageCPU(BaseModel):
    """CPU 资源使用情况"""
    totalCores: float = Field(..., description="总核心数")
    usedCores: float = Field(..., description="已使用核心数")
    usagePercent: float = Field(..., description="使用百分比")


class ResourceUsageMemory(BaseModel):
    """内存资源使用情况"""
    totalBytes: int = Field(..., description="总内存字节数")
    usedBytes: int = Field(..., description="已使用内存字节数")
    usagePercent: float = Field(..., description="使用百分比")


class ResourceUsage(BaseModel):
    """资源使用情况"""
    cpu: ResourceUsageCPU = Field(..., description="CPU 资源使用")
    memory: ResourceUsageMemory = Field(..., description="内存资源使用")


class NodeStatusItem(BaseModel):
    """节点状态项"""
    status: str = Field(..., description="节点状态")
    count: int = Field(..., description="节点数量")


class OverviewData(BaseModel):
    """概览数据结构"""
    clusterInfo: ClusterInfo = Field(..., description="集群信息")
    resourceUsage: ResourceUsage = Field(..., description="资源使用情况")
    nodeStatusSummary: List[NodeStatusItem] = Field(..., description="节点状态汇总")


class WorkloadItem(BaseModel):
    """工作负载项"""
    name: str
    namespace: str
    status: Optional[str] = None
    replicas: Optional[int] = None
    ready_replicas: Optional[int] = None
    created_at: Optional[datetime] = None


class WorkloadListResponse(BaseModel):
    """工作负载列表响应"""
    total: int
    page: int
    limit: int
    items: List[Dict[str, Any]]


class ResourceDetailResponse(BaseModel):
    """资源详情响应"""
    metadata: Dict[str, Any]
    spec: Optional[Dict[str, Any]] = None
    status: Optional[Dict[str, Any]] = None


class ResourceCreateRequest(BaseModel):
    """创建资源请求"""
    name: str
    namespace: str
    resource_type: str
    body: Dict[str, Any]


class ResourceUpdateRequest(BaseModel):
    """更新资源请求"""
    name: str
    namespace: str
    resource_type: str
    body: Dict[str, Any]


class ResourceDeleteRequest(BaseModel):
    """删除资源请求"""
    name: str
    namespace: str
    resource_type: str
    grace_period_seconds: int = 0
