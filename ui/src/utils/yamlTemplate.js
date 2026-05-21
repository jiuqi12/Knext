// src/utils/yamlTemplates.js

export const yamlTemplates = {
  deployment: `apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 250m
              memory: 256Mi
`,

  statefulset: `apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: my-statefulset
  namespace: default
spec:
  serviceName: my-service
  replicas: 1
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
          volumeMounts:
            - name: data
              mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
    - metadata:
        name: data
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 1Gi
`,

  daemonset: `apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: my-daemonset
  namespace: default
spec:
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
`,

  job: `apiVersion: batch/v1
kind: Job
metadata:
  name: my-job
  namespace: default
spec:
  backoffLimit: 3
  template:
    spec:
      containers:
        - name: busybox
          image: busybox:latest
          command: ["echo", "Hello from Job"]
      restartPolicy: Never
`,

  cronjob: `apiVersion: batch/v1
kind: CronJob
metadata:
  name: my-cronjob
  namespace: default
spec:
  schedule: "0 */6 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: busybox
              image: busybox:latest
              command: ["echo", "Hello from CronJob"]
          restartPolicy: Never
`,

  pod: `apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  namespace: default
  labels:
    app: my-app
spec:
  containers:
    - name: nginx
      image: nginx:latest
      ports:
        - containerPort: 80
      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 250m
          memory: 256Mi
`,

  service: `apiVersion: v1
kind: Service
metadata:
  name: my-service
  namespace: default
spec:
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 80
  type: ClusterIP
`,

  ingress: `apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
  namespace: default
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: my-service
                port:
                  number: 80
`,

  configmap: `apiVersion: v1
kind: ConfigMap
metadata:
  name: my-configmap
  namespace: default
data:
  config.yaml: |
    key1: value1
    key2: value2
`,

  secret: `apiVersion: v1
kind: Secret
metadata:
  name: my-secret
  namespace: default
type: Opaque
data:
  username: YWRtaW4=
  password: cGFzc3dvcmQ=
`,

  namespace: `apiVersion: v1
kind: Namespace
metadata:
  name: my-namespace
`,

  pv: `apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-pv
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /data/pv
`,

  pvc: `apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
`,

  serviceaccount: `apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-serviceaccount
  namespace: default
`
}

// 模板分类配置
export const templateCategories = [
  {
    label: '工作负载',
    options: [
      { label: 'Deployment', value: 'deployment' },
      { label: 'StatefulSet', value: 'statefulset' },
      { label: 'DaemonSet', value: 'daemonset' },
      { label: 'Job', value: 'job' },
      { label: 'CronJob', value: 'cronjob' },
      { label: 'Pod', value: 'pod' },
    ]
  },
  {
    label: '网络',
    options: [
      { label: 'Service', value: 'service' },
      { label: 'Ingress', value: 'ingress' },
    ]
  },
  {
    label: '配置',
    options: [
      { label: 'ConfigMap', value: 'configmap' },
      { label: 'Secret', value: 'secret' },
    ]
  },
  {
    label: '存储',
    options: [
      { label: 'PersistentVolume', value: 'pv' },
      { label: 'PersistentVolumeClaim', value: 'pvc' },
    ]
  },
  {
    label: '安全',
    options: [
      { label: 'ServiceAccount', value: 'serviceaccount' },
    ]
  },
  {
    label: '集群',
    options: [
      { label: 'Namespace', value: 'namespace' },
    ]
  },
]
