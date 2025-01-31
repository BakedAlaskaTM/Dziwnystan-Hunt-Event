txt_file = open("track_info_map_obsolete.txt", "r", encoding="UTF-8")

data = []

for line in txt_file:
    info = line.split("@")
    data.append([info[0], info[1], info[2], info[3], info[4].split("\n")[0]])

data.sort(key=lambda x: x[4])

track_info_file = open("track_info_map_temp.txt", "w", encoding="UTF-8")
for track in data:
    track_info_file.write(f"{track[0]}@{track[1]}@{track[2]}@{track[3]}@{track[4]}\n")
track_info_file.close()

