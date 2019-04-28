import os

class FileSystemOperations:
    arr_dirs = []  # TODO optimize   id: 12
    max_dir_depth = 0

    def get_dir_depth(self, dir, level=1):
        if os.path.isdir(dir):
            for d in os.listdir(dir):
                if level > self.max_dir_depth:
                    self.max_dir_depth = level
                dir_name = os.path.join(dir, d)
                if os.path.isdir(dir_name):
                    self.arr_dirs.append([level, d, dir_name])
                    self.get_dir_depth(dir_name, level + 1)
