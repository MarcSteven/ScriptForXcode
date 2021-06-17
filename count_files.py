import os
result = []

def get_all_file(cwd):
    get_dir = os.listdir(cwd)
    for i in get_dir:
        sub_dir = os.path.join(cwd,i)
        if os.path.isdir(sub_dir):
            get_all_file(sub_dir)
        else :
            ax = os.path.basename(sub_dir)
            result.append(ax)
            print(len(result)



if __name__ == "__main__":
    current_path = os.os.getcwd()
    get_all_file(current_path)




