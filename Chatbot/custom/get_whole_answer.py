def get_wanted_whole_answer(answer, file_path):
    wanted_context = open(file_path, "r").read().split("-#-")

    for i in wanted_context:
        if answer in i:
            return i
