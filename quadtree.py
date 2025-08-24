# quadtree.py
import math

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

    def contains(self, point):
        return (self.x <= point[0] < self.x + self.width and
                self.y <= point[1] < self.y + self.height)

    def intersects(self, other):
        return not (self.x >= other.x + other.width or
                    other.x >= self.x + self.width or
                    self.y >= other.y + other.height or
                    other.y >= self.y + self.height)

class Quadtree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []           # list of (x,y)
        self.car_map = {}          # (x,y) -> car
        self.divided = False
        self.nw = self.ne = self.sw = self.se = None

    def insert(self, point, car=None):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity and not self.divided:
            self.points.append(point)
            if car is not None:
                self.car_map[point] = car
            return True

        if not self.divided:
            self.subdivide()

        return (self.nw.insert(point, car) or self.ne.insert(point, car) or
                self.sw.insert(point, car) or self.se.insert(point, car))

    def subdivide(self):
        x, y = self.boundary.x, self.boundary.y
        w2, h2 = self.boundary.width / 2, self.boundary.height / 2
        self.nw = Quadtree(Rectangle(x,       y,       w2, h2), self.capacity)
        self.ne = Quadtree(Rectangle(x + w2,  y,       w2, h2), self.capacity)
        self.sw = Quadtree(Rectangle(x,       y + h2,  w2, h2), self.capacity)
        self.se = Quadtree(Rectangle(x + w2,  y + h2,  w2, h2), self.capacity)
        self.divided = True

    def remove(self, point):
        # remove point and mapping from this node if present
        if point in self.points:
            self.points.remove(point)
            self.car_map.pop(point, None)
            return True
        # recurse
        if self.divided:
            return (self.nw.remove(point) or self.ne.remove(point) or
                    self.sw.remove(point) or self.se.remove(point))
        return False

    def _collect_points(self, out):
        out.extend(self.points)
        if self.divided:
            self.nw._collect_points(out)
            self.ne._collect_points(out)
            self.sw._collect_points(out)
            self.se._collect_points(out)

    def find_k_nearest(self, query_point, k=5):
        # simple but effective: collect, compute dists, n-smallest
        all_pts = []
        self._collect_points(all_pts)
        all_pts.sort(key=lambda p: math.hypot(p[0]-query_point[0], p[1]-query_point[1]))
        return all_pts[:k]

    def get_car_at_location(self, location):
        # try exact key; for floats this is fine since we inserted exact tuples
        if location in self.car_map:
            return self.car_map[location]
        # search children if needed
        if self.divided:
            return (self.nw.get_car_at_location(location) or
                    self.ne.get_car_at_location(location) or
                    self.sw.get_car_at_location(location) or
                    self.se.get_car_at_location(location))
        return None
