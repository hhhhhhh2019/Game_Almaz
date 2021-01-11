class Queue:
    def __init__(self, v):
        self.values = v

    def push(self, v):
        self.values.insert(0, v)

    def pop(self):
        return self.values.pop(-1)

    def __len__(self):
        return len(self.values)


class BFS:
    graph = {}

    def __init__(self, g: dict):
        self.graph = g

    def is_neighbor(self, p, n):
        if n in self.graph[p]:
            return True

        return False

    def neighbors(self, p):
        return self.graph[p]

    def all_paths(self, start, goal):
        q = Queue([start])
        path = {}
        find = False
        iters = 0
        while not find:
            iters += 1
            if len(q) < 1:
                return
            p = q.pop()
            path[p] = self.neighbors(p)
            for i in self.neighbors(p):
                if i == goal:
                    find = True
                    break

                if not i in path and not i in q.values:
                    q.push(i)

            if iters > 2000:
                return

        return path

    def path(self, start, end):
        all_path = self.all_paths(start, end)
        finish = False
        path = []
        point = end
        iters = 0
        if all_path:
            while not finish:
                for i in all_path:
                    if self.is_neighbor(i, point) and not i in path:
                        path.append(point)
                        point = i
                        if point == start:
                            finish = True
                            path.append(point)
                        break

                iters += 1
                if iters > 2000:
                    break

        path.reverse()

        return path

    def __iter__(self):
        return iter(self.graph)