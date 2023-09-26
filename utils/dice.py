import random
from collections import deque


def roll(num_faces):
    # 生成0到num_faces-1的随机索引
    random.randint(0, num_faces - 1)
    weights = [1] * num_faces
    face = random.choices(population=range(1, num_faces + 1), weights=weights)[0]

    # 检查重复度
    recent_results = deque(maxlen=10)
    if face in recent_results and len(set(recent_results)) < 3:
        return roll(num_faces)
    recent_results.append(face)
    return face


def xdy(times, numFaces):
    times = int(times)
    numFaces = int(numFaces)
    a = 0
    b = []
    for i in range(times):
        d = roll(numFaces)
        a += d
        b.append(str(d))
        if not i == int(times)-1:
            b.append("+")
    if times == 1:
        result = ""
    else:
        result = "(" + ''.join(b) + ")"
    reply = {
        "equation": result,
        "result": str(a)
    }
    return reply

