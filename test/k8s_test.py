from app.core.k8s_client import get_custom_objects_api, get_core_v1_api
from app.utils.parse import parse_cpu, parse_mem

custom_objects = get_custom_objects_api()
apps_v1 = get_core_v1_api()

metrics_list = custom_objects.list_cluster_custom_object(
    group='metrics.k8s.io',
    version='v1beta1',
    plural='nodes'
)

for metrics in metrics_list['items']:
    print(parse_cpu(metrics['usage']['cpu']))
    print(parse_mem(metrics['usage']['memory']))
    # print(metrics['usage']['cpu'])
    # print(metrics['usage']['memory'])
    print("-------------------------------------------------------------------------------")