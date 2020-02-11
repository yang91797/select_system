import pickle
import os


def information(path, m, message=None):
    f = open(path, mode=m)
    if m == 'rb':
        return pickle.loads(f.read())
    if m == 'wb':
        new_path = '%s.new' % path
        f1 = open(new_path, mode='wb')
        f1.write(pickle.dumps(message))
        f1.close()
        f.close()
        os.remove(path)
        os.rename(new_path, path)
    if m == 'ab':
        f.write(message)
    f.close()

