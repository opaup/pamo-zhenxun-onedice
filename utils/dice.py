import random
from collections import deque


async def roll(num_faces):
    # 生成0到num_faces-1的随机索引
    random.randint(0, num_faces - 1)
    # weights = [1] * num_faces
    weights = []
    for i in range(num_faces):
        weights.append(random.uniform(0.001, 0.7))
    # print(rf"weights = {weights}")
    face = random.choices(population=range(1, num_faces + 1), weights=weights)[0]

    # 检查重复度
    recent_results = deque(maxlen=3)
    if face in recent_results and len(set(recent_results)) < 3:
        return roll(num_faces)
    recent_results.append(face)
    return face


async def xdy(times, numFaces):
    times = int(times)
    numFaces = int(numFaces)
    a = 0
    b = []
    for i in range(times):
        d = await roll(numFaces)
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

