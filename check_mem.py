from gc import mem_alloc, mem_free


def check_mem(message):
    free = mem_free()/1024
    alloc = mem_alloc()/1024
    print('{} - Memory free: {:.2f}kb / {:.2f}kb ({:.2f}%)'.format(message, free, free+alloc, 100*free/(free+alloc)))