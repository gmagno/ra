
import numpy as np
import quaternion as qua

from ra.tessellation import SphereTessellator


class Source():
    def __init__(self, position=(0, 0, 0), direction=(0, 0, 0)):
        self.position = np.array(position, dtype=np.float32)
        self.direction = np.array(direction, dtype=np.float32)


class SingleRaySource(Source):
    def __init__(self, position=(0, 0, 0), direction=(1, 0, 0)):
        super(SingleRaySource, self).__init__(position, direction)
        self.ris = np.array([position,], dtype=np.float32)
        self.rds = np.array([direction,], dtype=np.float32)


class IsotropicSource(Source):
    def __init__(self, position=(0, 0, 0), direction=(1, 0, 0), depth=1):
        super(IsotropicSource, self).__init__(position, direction)
        tess = SphereTessellator(
            # nverts=12,
            depth=depth
        )
        self.rds, self.indices = tess.sphere
        self.ris = np.zeros(self.rds.shape, dtype=np.float32)
        self.ris[:] = self.position


class CircleSource(Source):
    def __init__(self, nverts, position=(0, 0, 0), direction=(0, 1, 0), tol=1e-5):
        super(CircleSource, self).__init__(position, direction)
        a = 2 * np.pi / nverts
        a = np.arange(0.0, 2*np.pi, 2*np.pi/nverts)
        self.rds = np.zeros((nverts, 3), dtype=np.float32)
        self.rds[:, 0] = np.cos(a)
        self.rds[:, 2] = -np.sin(a)
        self.rds /= np.linalg.norm(self.rds)
        self.ris = np.zeros((nverts, 3), dtype=np.float32)
        self.ris[:] = self.position

        direction = np.array(direction, dtype=np.float32)
        direction /= np.linalg.norm(direction)

        dot = np.dot([0, 1, 0], direction)
        if dot + 1 < tol:
            q = np.quaternion(0, 0, 1, 0)
        elif dot -1 > tol:
            q = np.quaternion(1, 0, 0, 0)
        else:
            vcross = np.cross([0, 1, 0], direction)
            q = np.quaternion(1, 0, 0, 0)
            (q.x, q.y, q.z), q.w = vcross, (dot+1.0)
            q = q.normalized()

        rotmat = qua.as_rotation_matrix(q)
        self.rds = self.rds.dot(rotmat.T)



class ConicSource(Source):
    def __init__(self,
            radius, nverts, position=(0, 0, 0), direction=(1, 0, 0), tol=1e-5
    ):
        super(ConicSource, self).__init__(position, direction)
        a = np.random.rand(nverts) * 2 * np.pi
        r = radius * np.sqrt(np.random.rand(nverts))
        self.rds = np.ones((nverts, 3), dtype=np.float32)
        self.rds[:, 1] = r * np.sin(a)
        self.rds[:, 2] = r * np.cos(a)
        self.rds /= np.linalg.norm(self.rds)
        self.ris = np.zeros((nverts, 3), dtype=np.float32)
        self.ris[:] = self.position

        direction = np.array(direction, dtype=np.float32)
        direction /= np.linalg.norm(direction)

        dot = np.dot([1, 0, 0], direction)
        if dot + 1 < tol:
            q = np.quaternion(0, 0, 1, 0)
        elif dot -1 > tol:
            q = np.quaternion(1, 0, 0, 0)
        else:
            vcross = np.cross([1, 0, 0], direction)
            q = np.quaternion(1, 0, 0, 0)
            (q.x, q.y, q.z), q.w = vcross, (dot+1.0)
            q = q.normalized()

        rotmat = qua.as_rotation_matrix(q)
        self.rds = self.rds.dot(rotmat.T)
