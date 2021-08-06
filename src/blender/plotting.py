import cmath

import bpy


def plot(name, vertices):
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    scene = bpy.data.scenes[0]
    scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    edges = []
    for index, vertex in enumerate(vertices):
        if index > 0:
            edges.append((index - 1, index))
    faces = []
    mesh.from_pydata(vertices, edges, faces)
    mesh.validate()


T_UPPER_BOUND = 10
GRANULARITY = 0.001

vertices = []
samples = [GRANULARITY * i for i in range(round(T_UPPER_BOUND / GRANULARITY))]
for t in samples:
    result = -t * cmath.exp(-2j * cmath.pi * (t ** 2))
    vertices.append((result.real, result.imag, t))

plot("mersh", vertices)
