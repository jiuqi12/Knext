# 单位转换解析工具

def parse_cpu(cpu: str) -> float:
    """
    将cpu字符串转换为核心数目
    例如：100m -> 0.1
    """
    if cpu.endswith("n"):
        return round(float(cpu[:-1]) / 1e9, 2)    # 纳核
    elif cpu.endswith("u"):
        return round(float(cpu[:-1]) / 1e6, 2)    # 微核
    elif cpu.endswith("m"):
        return round(float(cpu[:-1]) / 1000, 2)   # 毫核
    else:
        return round(float(cpu))               # 核


def parse_mem(memory: str) -> float:
    """
    将内存字符串转换成Gi
    例如：512Mi -> 0.5Gi
         1G -> 1
    """
    if memory.endswith("Ki"):
        return round(float(memory[:-2]) / 1024 / 1024, 2)
    elif memory.endswith("Mi"):
        return round(float(memory[:-2]) / 1024, 2)
    elif memory.endswith("Gi"):
        return round(float(memory[:-1]), 2)
    else:
        return round(float(memory), 2)
