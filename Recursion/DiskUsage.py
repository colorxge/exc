import os


def disc_usage(path):
    total = os.path.getsize(path)
    print('{}:{}'.format(path, total))
    if os.path.isdir(path):
        for chird_dir in os.listdir(path):
            if os.path.isdir(chird_dir):
                dir_size = os.path.getsize(chird_dir)
                print('{}:{}'.format(chird_dir, dir_size))
                total += disc_usage(chird_dir)
            else:
                total += os.path.getsize(chird_dir)


# print(disc_usage('C:\\app'))


def disk_usage(path):
    """Return the number of bytes used by a file /folder and any descendents."""
    total = os.path.getsize(path)
    if os.path.isdir(path):
        for filename in  os.listdir(path):
            childpath = os.path.join(path, filename)
            total += disc_usage(childpath)

    print('{0:<7}'.format(total), path)
    return total


print(disc_usage('C:\QMDownload'))