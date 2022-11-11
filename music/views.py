from botocore.paginate import Paginator
from django.shortcuts  import render
from django.core.paginator import Paginator
from music.models import Song_store

# def show_song(request):
#     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
#
#     return render(request, "music.html")
#
def show_song(request):

    try:
        page = int(request.GET.get('page',1))
        if page<1:
            print("-----",page)
            page = 1
    except Exception:
        print("----")
        page = 1
    # print(page)
    all_song = Song_store.objects.all()

    paginator = Paginator(all_song, 20)
    page_song_list = paginator.page(page)
    page_num = paginator.num_pages

    if page_song_list.has_next():
        next_page = page + 1
    else:
        next_page = page
    if page_song_list.has_previous():
        pre_page = page - 1
    else:
        pre_page = page - 1
    return render(request, "music.html", {
        "songlist": page_song_list,
        "cur_page": page,
        "page_num": range(page, min(page_num + 1, page + 5)),
        "pre_page": pre_page,
        "next_page": next_page
    })