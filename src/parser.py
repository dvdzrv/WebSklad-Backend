def parse():
    string = ""
    with open("csv/tabulka.csv", "r", encoding="utf-8") as file:
        for line in file:
                line = line.replace(",,", ",NULL,").replace(" ", ";").replace(",", " ").replace("\"", "").split()
                line[0] = "NULL"
                line[1] = "'" + line[1].replace(";", " ") + "'"
                if not (line[2] == "NULL"):
                      line[2] = "'" + line[2] + "'"
                line[3] = "'" + line[3] + "'"
                line[4] = "'" + line[4] + "'"
                line[5] = "'" + line[5] + "'"
                string +=("(" + line[0] + "," + line[1]+ "," + line[2]+ "," + line[3]+ "," + line[4]+ "," + line[5] + ",NULL" + ")" + ",")


    return string[:len(string)-1]

if __name__ == "__main__":
    print(parse())