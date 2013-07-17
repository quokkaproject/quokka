def get_password(f):
    try:
        return open('.%s_password.txt' % f).read().strip()
    except:
        return
